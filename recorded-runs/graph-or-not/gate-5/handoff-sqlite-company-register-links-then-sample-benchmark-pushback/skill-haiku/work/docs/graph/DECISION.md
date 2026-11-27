# Graph decision

Decision: need-more-information

The integrity unit asks whether its 6-link questions over a 48M-entity, 310M-relation register in one 41 GB SQLite file should move to a graph database, an in-memory graph library, recursive SQL or no graph, under a 10 s budget. The two SQL runs on record took 14 min and 3 min 20 s (84 and 20 times the budget), but both carry query-shape waste that a rewrite removes, and that rewrite has not been run; whether SQL or a graph database fits turns on how many real calls reach the few hub entities, which neither the request nor the repo records.

## Workload facts

- Register of 48M entities and 310M relations of 11 kinds, in one SQLite file of 41 GB on a 64 GB RAM analysis server (stated by the user); the 11 kinds are listed in the comment in `db/schema.sql`.
- Entity kinds are company, person, public_body and address (CHECK constraint, `db/schema.sql`), so a walk of several links crosses kinds.
- Budget: under 10 s per question; 25 analysts ask new questions daily, mixing relation kinds and dates (stated by the user).
- Depth: 6 links (stated by the user). `linked_within` in `investigate/queries.py` defaults to `max_hops=6` and follows a relation in either direction.
- `linked_within` is a recursive CTE with `UNION ALL` that carries a path string; it returns one row per route, and its path check rejects a repeat only within a single route (`investigate/queries.py`). The same pattern returned 40 rows where `UNION` returned 10 on a test graph (`references/engines.md`, SQLite 3.53.1, executed).
- It does not filter on `since` or `until`. The other canned query, `directors_of`, filters on `until IS NULL` (`investigate/queries.py`).
- Indexes on `relation` are `(src, kind)` and `(dst, kind)` only (`db/schema.sql`). Neither carries the far endpoint, so each step also reads the row for the other end.
- The join condition `r.src = reach.id OR r.dst = reach.id` is not checked against a plan here (unknown; see below).
- Links per entity on average: 2 × 310M / 48M = 12.9 (derived from the stated counts; each relation has two ends).
- A typical start at average degree: 12.9^3 = 2,150 routes at 3 links and 12.9^6 = 4.6M routes at 6 links (derived; an average, not measured, and it understates the tail).
- Hubs: a few addresses and company-formation agents have hundreds of thousands of links (stated by the user). If a 300,000-link hub's neighbours average 12.9 links, its second hop alone gives 300,000 × 12.9 = 3.9M rows (derived).
- Upper bound on distinct entities reached within 6 links: 48M (derived from the stated count).
- Measured on the full data by the user: `linked_within` at 6 links, killed after 14 min (840 s, 84 times the budget), with indexes and the path check (stated by the user; one run, no failure rate). Level-by-level search from both ends in Python, one query per level, 3 min 20 s (200 s, 20 times the budget) (stated by the user).
- Neo4j two-week trial on a copy: the same 6-link questions took 2 to 8 s; analysts wrote their own patterns after a day (stated by the user). Neo4j version, Cypher version, copy size and concurrency are not stated (unknown).
- networkx load estimated at 95 GB (stated by the user). That is about 306 bytes per relation (95 GB / 310M, derived). At that rate one 64 GB copy holds about 209M of the 310M relations (derived).
- Compact layout, arithmetic only and not measured: each relation end stored as a 4-byte id in both directions is about 2.5 GB before attributes and offsets (derived from integer ids in `db/schema.sql`).
- Storage: the 41 GB file leaves about 23 GB of the 64 GB machine for everything else (derived). Whether 25 concurrent walks keep the working set in cache is unknown.
- Freshness: the register is loaded by a weekly import from the data team's repo (`README.md`); no continuous change is recorded.
- Counter-proposal tested (measured): `var/sample.db` is not in the repo, so a synthetic copy was built with `tools/make_sample.py` in a scratch folder (20,000 entities, 60,000 relations, average degree 6; SQLite 3.53.1, opened `mode=ro`; indexes `relation_src` and `relation_dst` present). `linked_within` at 6 hops with an unreachable target, so the whole walk runs, over 20 random starts: p50 0.158 s, max 0.307 s, timed with a Python clock. From one start, 50,866 route rows at 6 hops reach 17,208 distinct entities (same copy).
- Scaling the counter-proposal to the register (derived; a linear extrapolation, not a measurement): 12.9^6 = 4.6M routes from an average start, about 90 times the 50,866 measured on the sample at the same depth (4.6M / 50,866). At 0.158 s p50 that is about 14 s, before hub starts and before cache misses on a 41 GB file. The sample is 60,000 of 310M relations (about 1 in 5,200), so a sample pass says nothing about the register.
- Proposed alternative: tune SQLite (stated by the user, attributed to Wim). The tuning beyond the indexes and the path check is not recorded.
- Copy in the repo: none. `var/` is gitignored, no `registry.db` is present, and `tools/make_sample.py` builds only a synthetic 20,000-entity sample. Nothing was measured here. `docs/graph/CONTEXT.md` is absent, so the production SQLite version and read-only policy are not recorded.
- unknown: share of real 6-link calls that reach a hub within three links of an endpoint; distinct entities reached per call; p50, p95 and timeout count for `linked_within` over real calls, with the total call count; the query plan of the `OR` join on the full file; the Neo4j trial's version, Cypher version, copy size and concurrency; whether analysts need `since` and `until` filters on each link.

## Options considered

- graph-database (Neo4j, from the user's trial): not chosen and not rejected yet. The 2 to 8 s trial is the only measured result that meets the 10 s budget, but it is not shown for the full 310M-relation set, at 25 concurrent users, or on a stated version. The profile is partly met: deep ad hoc traversal, online with a 10 s budget, and a set too large for a copy per process. The churn part is absent (weekly import). Adoption costs a second stateful server, a feed from the weekly import that can drift, and a new query language (`references/engines.md`: Neo4j facts are documentation, not executed). Waits on the facts below.
- in-process-library (networkx, as the request proposed): rejected for networkx, because its estimated 95 GB exceeds the 64 GB RAM before any second copy is counted (stated by the user; derived above). A compact array layout is not measured, so it is not shown to hold and is passed over for now.
- recursive-sql (SQLite, `linked_within` or a rewrite): not chosen and not rejected. Both measured runs show the waste the skill names, a route-per-row `UNION ALL` and a query issued per level from Python. A one-statement, node-deduplicated, bidirectional version has not been run, so it does not count as holding yet. Storage alone is not shown to fail: the 41 GB file fits in 64 GB. Whether it holds depends on the first fact below.
- no-graph (plain joins): rejected. `linked_within` crosses the relation table up to six times, so it is a traversal. Lookups such as `directors_of` need no graph, but they are not the question asked.

## What would change the decision

1. Share of real 6-link calls whose start or target has a hub within three links, and the distinct entities each reaches within three links. Get it from the analysts' query log for the last three months, then count distinct entities per call with a deduplicated query on a copy opened read-only (`file:PATH?mode=ro`). If most calls reach a small distinct set, recursive-sql moves ahead once a deduplicated one-statement version passes the 10 s test on the full file. If hub-touching calls are common, graph-database moves ahead. The 10 s budget and the cut-off between the two are for the integrity unit to set.
2. Latency and failures for `linked_within` on real calls: p50, p95 and timeout count, with the total number of calls over the same period as the denominator (the application's timing log). If p95 is under 10 s, nothing needs deciding. If over-budget calls cluster on hub starts, fact 1 decides. If they are spread across ordinary starts, the rewrite comes first.
3. Neo4j trial specification: the server version string, the Cypher version, whether the copy holds all 310M relations, and p95 for 25 concurrent analyst questions, with hub and non-hub questions timed separately (the trial's logs). Gate the spend on a full-size run at that concurrency meeting 10 s. A smaller copy or single-user timings cannot carry the decision.
4. The plan of `linked_within` on the full file, from `EXPLAIN QUERY PLAN` run read-only. A `SCAN` of `relation` under `RECURSIVE STEP` means every step reads the whole table, and the `OR` join is part of the cost. `SEARCH` on both indexes means the cost is row count, which fact 1 measures.
