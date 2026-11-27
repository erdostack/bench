# Graph decision

Decision: in-process-library

The question is whether the ECO impact screen needs a change now, or should move to a graph database as the upgrade contractor proposes, or to networkx in the ECO service. The decision recorded before (recursive-sql, with a stated p95 of 180 ms) no longer stands: after the Ostrava BOM merge, the screen's p95 is 1.3 s, over the agreed 800 ms limit. The agreed rule (stated by the user and Ines) therefore moves the walk into the ECO service's memory with networkx. The finding it turns on is 1,300 ms against 800 ms, about 1.6 times over the limit, with BOM lines up from 400,000 to 1,100,000.

## Workload facts

- Items: 95,000 (stated by the user; `db/schema.sql` `item`). Current item count after the Ostrava merge: unknown (not stated)
- BOM lines: 400,000 before the merge (stated by the user; `db/schema.sql` `bom_line`); 1,100,000 now (stated by the user, last week's Ostrava merge). Growth: 1,100,000 / 400,000 = 2.75 times (derived from the two figures). Lines per item before: 400,000 / 95,000 = 4.21 (derived); now: unknown, because the item count is not restated
- Question asked of the connections: every assembly that uses a changed item at any level, walking up the BOM with a path check to stop loops (`sql/where_used.sql`, `WITH RECURSIVE up`). Depth is data-dependent (the walk continues until no new parent is found on a route)
- Shape of the walk: `UNION ALL` with a path column, so the query returns one row per route, not one per assembly. Each row then goes through `MIN(lvl)` and `GROUP BY` in the outer query (`sql/where_used.sql`). Whether that multiplies rows on the real BOM is unknown: the count of routes and the distinct assemblies reached are not in the repo, and no plan was given
- Loops: PLM imports have produced loops (stated by the user); the path check stops a part already on its route (`sql/where_used.sql`); the test confirms the loop terminates on a small case and lists each assembly once (`tests/test_where_used.py`, run on SQLite in the earlier check, passed)
- Load: about 600 impact screens a day (stated by the user, before the merge; not restated). At the stated p95 for every call, that would be 600 x 1.3 s = 780 s of query time a day, against 600 x 180 ms = 108 s before the merge (both derived; upper-bound style figures, since most calls are below p95)
- Latency rule: stay on the recursive query while the impact screen's p95 stays under 800 ms; past that, move the walk into the ECO service's memory with networkx (stated by the user and Ines, agreed last spring)
- Present timing: p95 1.3 s (stated by the user, after the Ostrava merge), against 180 ms p95 recorded before the merge (stated by the user). Ratio: 1,300 / 180 = 7.2 times (derived). Against the limit: 800 / 1,300 = 0.62 of the limit, so 1.6 times over (derived). Headroom before the merge: 800 / 180 = 4.4 times (derived)
- Window and method behind the 1.3 s p95: not stated (unknown); the 180 ms figure's window and method were not stated either
- Prototype: Ana's in-memory prototype held all of it in 350 MB and answered in 20 ms (stated by the user; not in the repo, not run here). The size of the BOM the prototype was built on is not stated. If it was built on the 400,000 lines, linear scaling to 1,100,000 gives about 350 MB x 2.75 = 960 MB (derived, an extrapolation)
- Engine operated today: Postgres 16 replica in production; SQLite in tests (`README.md`). Both run `sql/where_used.sql`
- `requirements.txt` pins `networkx==3.7`; no module in the repo imports it (grep of the repo), so the library is already named but not used
- Indexes on the walk's join columns: `bom_line_component (component_id)` serves the upward step; the primary key `(parent_id, component_id)` covers the other direction (`db/schema.sql`)
- Freshness and writes: BOM changes come from PLM imports; the frequency and how stale the screen may be are not stated: unknown
- Measured in this check: the repo's test (`tests/test_where_used.py`) passed on SQLite in the earlier check. No production-size measurement was possible: `var/` is gitignored and the repo holds no data
- unknown: the real BOM depth and fan-out (tail and hubs); the route count against the distinct assemblies reached on the real data; the production plan and timing on the Postgres replica; the window and method behind the 1.3 s and the earlier 180 ms p95; the item count after the merge; the number of ECO service processes that would each hold a copy, and the memory limit per process; how often PLM imports change the BOM, and how stale the screen may be; how the 800 ms threshold was set beyond the owners' agreement
- `docs/graph/CONTEXT.md` does not exist in the repo

## Options considered

- graph-database (a dedicated graph store, the one the upgrade contractor pitched; no product named): rejected, because the walk runs over 1.1M BOM lines, which fit in one process by the prototype's footprint (350 MB before scaling, about 960 MB after, derived), so the edge set is not too large for a copy per process. A second stateful system would add backup, upgrade and paging cost, and a feed from PLM that can drift, and the freshness need is not stated
- in-process-library (networkx in the ECO service, as the agreed fallback): chosen, because the measured p95 of 1.3 s is over the agreed 800 ms limit, the rule names this move, and the prototype's stated 20 ms answer shows the footprint and latency are viable. Holds on memory only as an extrapolation; per-process memory and the reload cadence against freshness are still unknown, so the first step is to load the full 1.1M-line BOM in one process and time it
- recursive-sql (the recursive query on the Postgres replica): rejected for now, because the measured p95 of 1.3 s is over the 800 ms limit. A rewrite of the walk (for example, one that removes the repeated route rows) has not been run, so it does not reopen the rung; the decision would move back only if the rewrite is run and passes the limit
- no-graph (plain joins, no traversal): rejected, because the impact of a change depends on a walk up the BOM of data-dependent depth, not on a single join across a link table

## What would change the decision

- The impact screen's p95 on the production replica, measured over a stated window with the method written down, coming back under 800 ms: that would be a measured result for recursive-sql again, and the rewrite would have to be run and measured before the in-process move is reversed. The owners of the rule are the user and Ines
- The full 1.1M-line BOM loaded into one ECO service process, with its memory and load time measured against the process limit and the freshness the readers need: if the copy does not fit the limit or the reload misses freshness, the in-process option fails, and the next rung to test is graph-database
- A measured route count far above the distinct assemblies reached on the real BOM (read from the plan or a count): that points to a rewrite of the walk that removes the repeated rows, which should be run before the in-process move is reversed
- A requirement for whole-BOM analysis across all items (for example, every assembly's exposure to every part, in one batch): that is a whole-graph job for the in-process-library on a snapshot, not the online screen
