# Graph decision

Decision: in-process-library

The control room asks which depot can send the recovery truck with the least driving time (segment.minutes) on roads a 26-tonne lorry may use, and the AVL vendor asks whether a graph database should do that routing. The answer is a shortest-path walk of unknown depth over a network that fits in one process: 8,100 segments (stated by the user) load to about 4.5 MB, so the networkx library the app already uses can hold it, and the reported wrong depot comes from the weighting and the duplicate-pair handling in `recovery/nearest.py`, not from the choice of store.

## Workload facts

- The question asked of the connections is a least-cost path from a breakdown junction to each of 4 depots, weighted by minutes and excluding bus-gate segments for the lorry (stated by the user; `recovery/nearest.py` today uses `nx.shortest_path_length` with no `weight`, so it counts hops, and `load()` keeps only the last row when two segments join the same pair, which is how a bus-gate row can replace the legal road).
- Junctions: about 6,200 (stated by the user); unknown in the repo, since `var/roads.db` is gitignored and not present.
- Segments: about 8,100 (stated by the user), of which the repo says some pairs carry two segments (`db/schema.sql`, comment on `segment`). Distinct junction pairs are not counted anywhere in the repo.
- Depots: 4 (stated by the user; `db/schema.sql` `depot` table).
- Depth: unbounded in principle, bounded by the network diameter; no depth limit is set in the repo.
- Fan-out: unknown. Sizing assumes the average from the segment count: 2 x 8,100 / 6,200 is about 2.6 segment ends per junction (arithmetic from the stated figures).
- Measured, on a synthetic network of 6,200 junctions and 8,100 segments (300 of them parallel bus-gate rows) built to the stated sizes, with `recovery/nearest.py` loaded unchanged: `load()` traced memory 4.50 MB, 577 bytes per distinct edge (measured with `tracemalloc`, Python 3.13.18, networkx 3.7, SQLite 3.53.1); 30 `nearest_depot` calls at 25.6 ms each, reloading the graph on every call. Extrapolated from this sample, not measured on the real network.
- Load: about 30 breakdowns a day (stated by the user), so about 1 query per 48 minutes on average; no latency budget or peak rate is stated.
- Writes and freshness: not stated. The app rebuilds the graph from the table on each call, so readers see the table as it is at call time.
- What is operated today: the SQLite database `var/roads.db` (exported road network, per `README.md`), one Python process of the control-room app; the app already uses networkx (`README.md`). No graph database is run or named in the repo.
- What was measured or tried: no query log, no plan, no call counts, no failure rate. No previous remedy is recorded in the repo.
- unknown: the real `var/roads.db` was not in the repo, so real junction and pair counts, minute distribution and the number of bus-gate pairs were not measured. Searched: the repo root, `db/`, `recovery/`, `.gitignore` (which excludes `var/`). Also unknown: the freshness the control room needs, the latency budget, the number of processes that load the graph, and whether other code uses `load()`.
- Sum (stated by the user): 2 x segments / junctions = 2 x 8,100 / 6,200 = 2.6 segment ends per junction, average, from the stated figures.
- Sum (measured on the synthetic sample): 577 bytes per edge x 8,100 segments = about 4.7 MB for the full edge set, to compare with the 4.50 MB measured for 7,800 distinct pairs.

## Options considered

- graph-database (a dedicated graph store, the vendor's offer; the request does not name a product): rejected, because the whole profile is absent: the edge set is about 4.5 MB in one process at about 30 queries a day, nothing is measured failing, and the vendor's option would add a second stateful system and a feed from the system of record for a load the in-process structure handles in tens of milliseconds (see Workload facts).
- in-process-library (the edges loaded into memory): chosen, because the edge set fits in one process (measured about 4.5 MB for 7,800 distinct pairs; about 4.7 MB for 8,100 segments, extrapolated), a per-call reload took 25.6 ms in the measurement, and the library is already in the app (`README.md`). The fix is in the code: weight the path by `minutes`, drop `bus_gate = 1` rows for the lorry, and keep the minimum minutes per pair instead of the last row.
- recursive-sql (recursive queries on the database already run): rejected for now, because no recursive query runs today, no measurement shows a recursive minutes-weighted search meeting the need, and a recursive common table expression that returns every route would multiply rows at each level. The rung is not shown to hold, so it is passed over, not disproved.
- no-graph (plain joins, no traversal): rejected, because the question is a walk from a breakdown junction to the depots of unknown depth; a single join does not answer it.

## What would change the decision

- The real `var/roads.db` edge set grows to a size that a load per process no longer fits in the memory the control-room host gives the app, or the number of processes that load it grows; the memory limit is set by the control room, not the repo.
- A requirement appears for online routing to many more calls per minute (for example, all-pairs or live fleet dispatch) with a latency budget the reload cannot meet, measured on the real network; that would be the trial to run before any spend on a graph database.
- A freshness requirement shorter than the reload time per call, stated by the control room, with the graph rebuilt from a changing source; then a dedicated service that holds the structure and applies changes as they arrive would be the next thing to test, which is a datastore choice and not the vendor's offer as stated.
- Measured failure of the in-process approach at the real network size with a recorded total of calls, not a count of slow calls alone.

Nothing in the repo was changed.
