# Graph decision

Decision: in-process-library

The question was whether recovery/nearest.py, which sends the recovery truck from the wrong depot, needs the AVL vendor's graph database, a graph library, recursive SQL or no graph. The network is about 6,200 junctions and 8,100 segments, so a copy in memory costs roughly 6 MB, and the wrong answers come from the code (it counts hops, and it keeps one row per junction pair). The fix is to keep using NetworkX, which the app already uses, with a weighted search over truck-legal segments, and to adopt no new store.

## Workload facts

- Question asked of the connections: least-cost path from a breakdown junction to each of the depots, with cost = segment.minutes, a walk of data-dependent depth (recovery/nearest.py, nearest_depot).
- The code calls `nx.shortest_path_length(g, junction_id, at)` with no `weight=`, so it counts segments, not minutes (recovery/nearest.py).
- `load()` builds an `nx.Graph`, which holds one edge per junction pair. `add_edge` on an existing pair overwrites the attributes, so where a bus gate and an old road join the same two junctions, the row read last wins (recovery/nearest.py; db/schema.sql says two segments may join the same two junctions).
- `bus_gate` is loaded as an attribute but never used, so a 26-tonne lorry can be routed through bus gates (recovery/nearest.py, db/schema.sql: bus_gate 1 = buses, taxis and cycles only).
- The graph is rebuilt from the whole segment table on every call to nearest_depot (recovery/nearest.py).
- Stated by the user: the vehicle is a 26-tonne lorry and cannot use bus gates.
- Stated by the user: "nearest" means least driving time for the truck, segment.minutes.
- Stated by the user: about 6,200 junctions and about 8,100 segments.
- Stated by the user: 4 depots.
- Stated by the user: about 30 breakdowns a day.
- Stated by the user: the AVL vendor offers to put the road network in their graph database and route there.
- Size in memory: 8,100 edges loaded into a NetworkX 3.7 MultiGraph with minutes and bus_gate attributes on 6,200 synthetic nodes took about 6.2 MB traced (measured: tracemalloc on random edges, Python 3.12/3.13 environment; the real data was not available, so this is an extrapolation) and about 0.1 s to build.
- Load: 30 breakdowns a day is about one every 48 minutes over 24 hours (24 x 60 / 30 = 48), a batch-sized load even with the full reload per call.
- Writes and freshness: unknown: the file var/roads.db is not in the repo (it is gitignored), and nothing states how often segments or minutes change or how fresh an answer must be.
- unknown: latency budget for a depot decision, and how many processes would hold a copy. Looked in README.md, db/schema.sql and recovery/. There are no usage exports, benchmarks, migrations or decision records.
- unknown: whether any junction pair has more than two parallel segments, or whether any junction is reachable only through bus gates. The database copy is not in the repo.
- Not measured: query plans and real timings, because var/roads.db is absent. Nothing in the repo was run against real data.

## Options considered

- graph-database (the AVL vendor's graph database): rejected, because 8,100 edges is about 6 MB in memory and 30 calls a day is a small, batch-like load, so no copy-per-process limit or latency failure exists, and the problem is in how the code builds and searches the graph, which a new store would not fix.
- in-process-library (NetworkX, already used by the control-room app): chosen, because the data fits in a few MB (measured above), a reload takes about 0.1 s, and the defects are small changes in the existing code: use `nx.MultiGraph` or keep the cheapest legal segment per junction pair, drop `bus_gate = 1` segments (or filter them in the SQL), and pass `weight="minutes"` to the shortest-path call (a multi-source `nx.multi_source_dijkstra` from the four depots, or one Dijkstra from the breakdown junction, replaces the loop over depots). Cache the graph and reload it when the segment table changes.
- recursive-sql (recursive queries on the SQLite database): rejected, because no measurement or arithmetic shows it meets the need, and a weighted shortest path in recursive SQL means carrying path cost along every route while the library already does this in one call.
- no-graph (plain joins, no traversal): rejected, because the question is a shortest path of unknown depth between junctions, which is a walk along a relation between things of the same kind.

## What would change the decision

- The segment table changing so often that a cached graph cannot meet the freshness the control room needs (the control room's owner sets that limit) would move this to recursive-sql or a service that holds one shared graph.
- The network growing from about 8,100 segments to a count where one copy, measured on the real data (bytes per edge times edges), no longer fits comfortably in a process, or routing becoming a many-requests-a-second online service with a latency budget the library misses, would move this to graph-database. Run that trial on the full edge set and the real query mix first.
- Finding that the real data has junctions reachable only through bus gates, or no truck-legal path from some depot, does not change the option; it changes what nearest_depot should return (None), which the control room should decide.
