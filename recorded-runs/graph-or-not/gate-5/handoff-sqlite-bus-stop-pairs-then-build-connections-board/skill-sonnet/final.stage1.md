Decision: no-graph

No graph database, graph library or recursive SQL is needed. The Connections panel is a join: the routes at this stop and at the stop across the road, minus the school-only routes. The only stop-to-stop link is paired_stop_id, followed exactly one step. A bus network can be drawn as a graph, but this panel doesn't traverse it.

The numbers it turns on:
- Depth: one hop (stop to its pair), then the stop_route table. 41,000 rows over 6,900 stops is about 5.9 routes per stop.
- Load: 1,200 screens once a minute is 20 lookups a second, against a timetable rebuilt nightly.
- Measured: on a synthetic SQLite database of that size, the panel took about 0.07 ms on average and 12 ms at worst, over 3,000 random stops. It is random data, not your export, so treat it as order of magnitude.

How to build it (I did not change any code): write sql/connections.sql that takes the stop itself, the stop in its paired_stop_id, and any stop whose paired_stop_id is this stop. It joins stop_route and route, keeps school_only = 0, and returns each route once ordered by short_name. The reverse lookup matters because the export records each pair once, on one of the two stops only. If you read only the stop's own paired_stop_id, one side of every pair would miss the other side's routes. On my test, both stops of a pair returned identical lists. The existing routes_here query does not filter school-only routes, so don't reuse it as is.

Not found: the real number of pairs and the real share of school-only routes (the real export isn't in the repo). An index on stop(paired_stop_id) is the ordinary fix if the reverse lookup ever shows up in profiling; it isn't needed on these numbers. A graph or recursive approach would only be worth revisiting if a future panel needs multi-leg journeys or transfers more than one step away.

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
