Decision: graph-database

The outage trace has to return the set of nodes still fed when one segment opens, in 1.5 s p95 at about 900 traces an hour, on a grid of 2.9M nodes and 3.4M segments. The in-memory option does not fit: 2.1 GB for 6% of the network extrapolates to about 35 GB for the whole grid, against 16 GB per trace server. The closure table and the region split were tried and failed. The SQL in place is measured at 8.4 s p95, so a graph database is the choice on the evidence we have.

Before committing money, run one cheap test. Rewrite the trace to use a node-only `UNION` in place of the path array, which stops on loops and returns one row per node, and replay last January's storm with `EXPLAIN (ANALYZE, BUFFERS)`, counting distinct nodes beside the rows. If that meets 1.5 s p95, recursive SQL holds and this decision is withdrawn. If it does not, load the full edge set into the candidate graph database and run the real query mix at 900 traces an hour while the switching feed runs at about 0.52 changes a second.

The cost of a graph database is a second stateful system to back up and run, a feed from `netmodel` for every switching change, and a new query language. The trace's fed-set size is not in the repository and is the main unknown.

Nothing in the repository was changed except the new file `docs/graph/DECISION.md`.
