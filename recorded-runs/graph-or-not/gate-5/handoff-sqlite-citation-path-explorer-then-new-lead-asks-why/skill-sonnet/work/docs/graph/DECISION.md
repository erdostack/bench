# Graph decision

Decision: graph-database

The citation-path explorer runs a shortest-chain search of up to 6 hops over 410M citations between 96M papers, with year and retraction filters applied during the walk, for 400 staff on a 3 s p95 budget. SQLite measured 41 s p95 on a copy of the snapshot, and the in-memory options do not fit the hosts as run today (networkx about 53 GB per worker; the 6 GB array times 6 workers is 36 GB against 32 GB), so the dedicated graph database is the choice, to be gated by a trial on the full edge set with the real filters.

## Workload facts

- 410M citations between 96M papers in the SQLite snapshot (stated by the user)
- About 1.2M new citations a day, to be visible the next morning (stated by the user); 1.2M / 410M = 0.3% of the edges a day, 1.2M / 86,400 s = about 14 per second if spread evenly
- A search is the shortest chains between two papers, up to 6 hops, skipping retracted papers, optionally only through papers after year X (stated by the user); the filters apply during the walk, not afterwards (stated by the user)
- Budget is 3 s p95 with 400 staff using it (stated by the user)
- Average fan-out: 410M / 96M = 4.3 citations per paper (derived from the stated counts); the tail (hubs, highly cited papers) is unknown. A walk of 6 hops in both directions can reach 4.3 x 2 = 8.6 per step, so the reach at depth 6 is up to 8.6^6, about 400 million, which is in the order of the whole graph (derived upper bound from the average fan-out)
- The recursive query in sql/path.sql, with indexes both ways, runs 41 s p95 on a copy of the snapshot, 13.7 times over the 3 s budget (stated by the user; 41 / 3 = 13.7). The query builds both directions with `UNION ALL`, carries a path string and returns one row per route, so some of the 41 s is route repetition; the route count was not measured (sql/path.sql)
- networkx on a 20M-citation sample took 2.6 GB, so 2.6 GB x (410M / 20M = 20.5) = 53 GB for everything, per worker, against 6 workers on 32 GB hosts (stated by the user; citepath/config.py `WORKERS = 6`; citepath/paths.py loads the whole graph in each worker)
- Wen's compressed adjacency array in numpy fits in 6 GB and runs a search in 0.8 s, with the filters applied during the walk, but every new filter took her about two weeks to add, and a rebuild for the daily changes takes 40 minutes; the platform team said no to running it (stated by the user)
- Copies of that array in memory: 6 workers x 6 GB = 36 GB against a 32 GB host if each worker holds its own copy (derived from citepath/config.py and the stated sizes); whether the array can be shared between workers is unknown
- A closure table came out at about 90 billion rows (stated by the user); 90 billion / 410M edges = about 220 rows per edge, so it is not a remedy
- Sanne (the owner) wants to keep it all in SQLite with better indexes (stated by the user)
- Operated today: one SQLite file `var/snapshot.db`, refreshed daily from the open citation dump by `citepath/refresh.py` (not in the repo's file list); Python 3.12, networkx 3.7, numpy 2.3 (README.md, requirements.txt, db/schema.sql)
- Edge indexes: primary key (citing_id, cited_id) and `citation_cited` on (cited_id, citing_id); `paper.retracted` and `paper.year` are on the `paper` row, not on the edge (db/schema.sql)
- unknown: concurrency in practice (searches at once at peak), the share of searches that use the year filter, and the latency by hop count; only one p95 was given
- unknown: whether the daily changes need to be applied incrementally or only at an overnight window; "the next morning" suggests a window, but the repo states no hour
- unknown: the graph database engine, its version and its memory needs; not chosen here
- Nothing was run or measured by me (no database in the repo), and nothing in the repo besides this file was changed.

## Options considered

- graph-database (a dedicated graph store): chosen, because the traversal is up to 6 hops with filters applied mid-walk, online, over 410M edges, and the cheaper rungs are measured failing: SQLite at 41 s p95 against 3 s, the networkx copy at 53 GB per worker against 32 GB hosts, the closure table at 90 billion rows, and the per-worker copy of the 6 GB array at 36 GB against 32 GB. The costs are a second stateful system to run, a daily feed from the snapshot, and a new query language; its query language also takes the year and retraction filters as part of the walk, which the array needed two weeks of code for each. A graph database does not remove hubs, so the 6-hop limit and any cap on highly cited papers should be kept. Before money is committed, trial it on the full 410M-edge set, with the real mix of searches and filters, at the 400-staff load.
- in-process-library (edges loaded into memory): rejected, because networkx needs about 53 GB per worker against 32 GB hosts, and Wen's array needs 6 x 6 = 36 GB across the 6 workers as configured. The array does 0.8 s and its 40-minute rebuild fits "visible the next morning", so this rung is close, see below.
- recursive-sql (recursive queries on SQLite): rejected, because the running query with indexes both ways measured 41 s p95 against 3 s and the closure table is 90 billion rows. A rewrite nobody has run (for example visiting each paper once instead of one row per route) does not reopen this rung, and Sanne's "better indexes" are already in place on both ends.
- no-graph (plain joins, no traversal): rejected, because the search follows citations between papers for up to 6 hops.

## What would change the decision

- Wen's array held once per host (for example memory-mapped and shared by the 6 workers, 6 GB against 32 GB), measured on the real filters at 3 s p95 or under with 400 staff, and the platform team accepting a nightly 40-minute rebuild that finishes before the research office starts (the platform team's call), would move this to in-process-library. Today each worker holding its own copy is 36 GB against 32 GB.
- A rewritten SQLite query, measured on the copy of the snapshot at or under 3 s p95 for 6 hops with both filters, would move this to recursive-sql. Today it is 41 s.
- The trial on the full edge set failing the 3 s p95 with the real query mix would send the work back to the in-process array.
- The research office accepting fewer hops (a limit they set, today 6) could change which rung holds; it changes the question, so it needs the office's agreement.
