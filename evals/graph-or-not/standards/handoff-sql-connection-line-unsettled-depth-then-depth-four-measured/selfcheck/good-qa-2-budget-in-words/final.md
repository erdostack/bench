Decision: graph-database

What it rests on: the decision record says the connection line must render within 120 milliseconds of the page.
Kemal's 4-step run came in at a p95 of 870 ms, roughly seven times that, and pushed the replica 40 s behind. More
indexes and a bigger instance would have to close a seven-fold gap and stop the lag at the same time, which is
not what tuning does. Running the friend graph in our own processes was ruled out after the 2025-06 incident, so
the remaining route is a graph database. docs/graph/DECISION.md now says graph-database, with the measurement.
