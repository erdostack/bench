Decision: recursive-sql

Keep the network model in netmodel Postgres and change the trace from path enumeration to plain reachability. The slowness comes from the query's shape, not from SQL being the wrong tool for this.

Why:

- The trace asks which nodes stay reachable from the source with one segment removed. That is a set question. The current query carries a `path` array and uses `UNION ALL`, so it generates every simple path from the source, not every reachable node. In a meshed network with loops, the number of simple paths grows combinatorially. The `DISTINCT` at the end only hides that after the work is done.
- I checked this on a synthetic meshed grid in SQLite (a stand-in for the Postgres query, since the real data is not here). Same node sets both ways, very different work:

  | grid | path-array rows | path-array time | node-only UNION rows |
  |---|---|---|---|
  | 4x4 (16 nodes) | 1,056 | 0.007 s | 16 |
  | 5x5 (25 nodes) | 76,873 | 2.2 s | 25 |

  Both versions return the same reachable set (25 nodes in the 5x5 case). The node-only version does one row per node.
- The rewrite is small: drop `path`, use `UNION` instead of `UNION ALL`, and the recursion dedups against rows already produced, so it terminates on loops without the array check. The `= ANY(path)` test goes away. Keep the partial indexes on `segment (a_node)` and `segment (b_node)` where `is_closed`. Check the plan with `EXPLAIN (ANALYZE, BUFFERS)` to confirm the OR join uses both indexes as a bitmap OR.
- Stay in Postgres for the switching feed. 45,000 state changes a day are plain updates to `segment.is_closed`, with no sync step. The closure table was ruled out for exactly that reason, and a graph database would add a second store that has to track those same updates.
- Why not in-process-library: the 35 GB figure comes from networkx's per-object overhead on every node and edge. It does not measure the graph itself. A compact adjacency array (CSR) for 2.9M nodes and 3.4M segments would be far smaller. It is a real fallback. But it means a full copy per trace server, a live update path for 45,000 changes a day, and a rebuild story on every restart, all to speed up a query the database can already do with the right shape. Hold it in reserve if the measured p95 misses.
- Why not graph-database: nothing in the request needs what a dedicated graph database adds, and the cost is a new operational system on the control-room path.
- Regional splitting is already ruled out in the request (41% of storm traces cross regions), so it is not a candidate here.

What is not yet known, and why this is a pick and not a proven fix:

- I have not run the rewrite against Postgres or the real 2.9M-node, 3.4M-segment model. The storm replay is the test: run last January's storm through the rewritten query and measure p95 against the 1.5 s budget (900 traces an hour is about 0.25 per second).
- The cost of the rewrite scales with the size of the reachable set per trace, not with loops. For a source high in a big meshed area that set may be large. If the replay shows the reachable sets are the problem, the in-process option becomes the next thing to measure.

Next steps:

1. Replace `sql/outage_trace.sql` with the node-only `UNION` form. Drop the `path` column and the `ANY` check, and keep the final `SELECT node_id`.
2. Run `EXPLAIN (ANALYZE, BUFFERS)` on a representative source and opened segment, and confirm both segment indexes are used.
3. Replay last January's storm and report p95 against the 1.5 s budget.
4. If p95 still misses, measure a compact in-memory adjacency (CSR) on the same replay before deciding on anything heavier.
