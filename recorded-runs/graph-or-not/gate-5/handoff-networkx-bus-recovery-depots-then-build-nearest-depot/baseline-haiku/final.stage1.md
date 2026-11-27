Decision: in-process-library

Keep the routing in the control-room app and use networkx, which is already installed (3.7 here) and already used by the app. Do not adopt a graph database or move the routing to the vendor.

Why:
- The network is about 6,200 junctions and 8,100 segments, with 4 depots and about 30 breakdowns a day. The whole graph fits in memory and a single shortest-path query over it is cheap. A graph database solves a scale and concurrency problem this does not have.
- The actual faults are in nearest.py, not in the choice of tool:
  1. It uses shortest_path_length with no weight, so it counts segments. It must use weight="minutes".
  2. It loads every segment into nx.Graph. Where a bus gate runs beside an old road between the same two junctions, the later row overwrites the earlier one, so the answer depends on row order. For parallel segments, keep the minimum minutes.
  3. It never excludes bus gates. A 26-tonne truck must not use segments with bus_gate = 1, so drop those edges before routing.
- Recursive SQL could do this, but weighted shortest path is not a natural recursive query. It would mean writing an iterative Dijkstra in SQL, which is harder to test than the library code it replaces.
- "No graph" is wrong. Finding the least-time route to each depot is a graph traversal.

Suggested change (to be tested before release, not yet run here because the data file var/roads.db is not in the workspace):
- In load(conn), select only segments with bus_gate = 0, and for each (a, b) keep the smallest minutes.
- In nearest_depot, compute nx.single_source_dijkstra_path_length(g, junction_id, weight="minutes") once, then pick the depot with the smallest value among reachable depot junctions. Ties are resolved by depot_id order.
- Add tests with a small fixture: a parallel bus-gate segment that is faster and must be ignored, a parallel normal segment that is slower and must win, and a depot reachable only through a bus gate, which must return None.

Caveat: the reasoning above rests on the schema and code in this workspace and on the stated sizes. It has not been checked against the real roads.db.
