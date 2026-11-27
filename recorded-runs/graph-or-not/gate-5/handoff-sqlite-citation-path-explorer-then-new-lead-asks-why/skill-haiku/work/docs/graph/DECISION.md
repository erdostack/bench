# Graph decision

Decision: graph-database

The research office wants chains of up to 6 citations between two papers, skipping retracted papers and optionally only through papers after a year, at 3 s p95 for 400 staff, over 410M citations and 96M papers. The recursive query runs at 41 s p95 on a copy, so it is measured failing; the in-memory options do not fit as deployed (6 workers at 6 GB each is 36 GB on a 32 GB host, and networkx would need 53 GB per worker). A graph database is therefore the choice on the evidence, gated by two cheaper trials that could still overturn it: a shared, memory-mapped copy of Wen's array per host, and a bidirectional, early-exit rewrite of the SQL.

## Workload facts

- 410M citations and 96M papers in the SQLite snapshot (user stated, in the request; `db/schema.sql` has the tables, the counts are not in the repo).
- Search: shortest chains between two papers, up to 6 hops, skipping retracted papers, optionally only through papers after year X (user stated; `sql/path.sql` has `:max_hops`, `p.retracted = 0`, and no year filter yet).
- Budget: 3 s p95, 400 staff (user stated).
- Ingest: about 1.2M new citations a day, which is 13.9 a second on average (user stated; 1.2M / 86,400), visible the next morning (user stated), so the freshness needed is daily.
- Measured, recursive SQL: 41 s p95 on a copy of the snapshot, with the path array and indexes both ways (user stated). 41 / 3 = 13.7 times the budget.
- Measured, networkx: 2.6 GB for a 20M-citation sample (user stated), which is 130 bytes per citation (derived); 410M citations gives 53.3 GB (derived), per worker (user stated).
- Measured, numpy compressed adjacency: about 6 GB, 0.8 s (user stated), with the mid-walk year and retraction filters needing about two weeks of work each and the daily rebuild taking 40 minutes, which the platform team refused to run (user stated).
- Workers: 6 (`citepath/config.py`, `WORKERS = 6`), on 32 GB hosts (user stated). Six copies of a 6 GB array is 36 GB on a 32 GB host (derived), so one copy per worker does not fit; the copies would have to be shared to fit.
- Closure table: about 90 billion rows (user stated), so it is closed.
- Average citation degree, undirected: 2 × 410M / 96M = 8.5 neighbours per paper (derived). Random-graph estimate of the reach by hop: 9, 73, 623, 5,300, 45,000, 388,000 papers at hops 1 to 6 (derived). This is an approximation; citation graphs have hubs, so the true reach is larger and must be measured.
- Bidirectional search meeting at hop 3 from each end: about 623 papers per side on average (derived, same approximation). This is the size of the required set if the walk stops at the meeting depth.
- Measured in the SQL: the recursive part carries the full path as a string and uses `UNION ALL`, so each route is a row, and it walks to `:max_hops` before the `LIMIT 5` ranks the results, so the walk does not stop at the first hit (`sql/path.sql`; a structural fact, the row count is not measured).
- Operated today: SQLite snapshot, refreshed daily from the open citation dump by `citepath/refresh.py` (`README.md`).
- unknown: the search rate across the 400 staff, and so the calls per second (only the staff count is stated).
- unknown: the true reach of a hub paper (the heavy tail of citation counts), which the random estimate does not capture.
- unknown: whether Wen's 0.8 s includes the year and retraction filters.
- unknown: whether the six workers are processes or threads, and so whether a single memory-mapped copy can be shared across them.
- unknown: the real route count and distinct count for the 41 s query (no plan or count in the repo).
- not measured: any plan or timing on the real snapshot in this check (the copy is not in the checkout).

## Options considered

- graph-database (a dedicated graph store): chosen, because the search is a walk of up to 6 hops with an online budget of 3 s p95 for 400 staff, the edges do not fit per worker in memory (53 GB per worker for networkx, and 36 GB across six copies of Wen's array), and the recursive SQL is measured at 41 s p95. The cost: a second stateful system to back up, upgrade and be paged for, an ingest of 1.2M citations a day from the dump that can drift, and a new query language. The rebuild and ingest are daily, which a graph store handles.
- in-process-library (the edges loaded into memory): rejected as deployed, because Wen's array meets the time (0.8 s) but six copies at 6 GB each do not fit 32 GB hosts (36 GB), and the networkx copy is 53 GB per worker. It is the strongest alternative: one shared, memory-mapped copy per host would fit (6 GB of 32 GB), but that is untested, and the year and retraction filters take about two weeks each and the platform refused the daily rebuild.
- recursive-sql (recursive queries on the SQLite snapshot): rejected for now, because the query is measured at 41 s p95 against 3 s, which is measured failing. A rewrite that stops at the first meeting depth, uses a visited set in place of the path string, and filters early would cut the work, but nobody has run it, so it does not reopen this rung on the evidence we have. It is the first trial below.
- no-graph (plain joins, no traversal): rejected, because the question is a chain of up to 6 citations, which is a walk across a relation between papers of the same kind.

Trials that gate the spend, in this order, each on a copy of the snapshot: (1) the bidirectional, early-exit rewrite of `sql/path.sql` (visited set, meet in the middle at 3 hops, year and retraction filters applied in the walk), measured with `EXPLAIN (ANALYZE, BUFFERS)` or the SQLite equivalent, against 3 s p95 on a replay of real searches; if it meets 3 s, recursive-sql holds and this decision is withdrawn. (2) If it does not, a memory-mapped copy of Wen's array shared by the six workers on one 32 GB host, with the filters in the walk, measured against 0.8 s and the daily rebuild time; if it meets both, in-process-library holds. (3) If neither passes, load the full edge set into the candidate graph database and run the real search mix with the 1.2M-a-day ingest.

## What would change the decision

- The rewrite in trial (1) meeting 3 s p95 on real searches would move this to recursive-sql, since the 41 s would then be walk waste and not storage. Sanne, as owner, decides whether the replay counts as the test.
- A memory-mapped array shared across the workers, measured at 0.8 s with the filters on and the daily rebuild inside the refresh window, would move this to in-process-library, since the platform's objection to the rebuild would then need a new answer. The platform team's call is that objection.
- A measured hub reach that makes the walk exceed 3 s p95 in any shared-array layout would keep the decision at graph-database.
- Nothing in the repository was changed other than this file.
