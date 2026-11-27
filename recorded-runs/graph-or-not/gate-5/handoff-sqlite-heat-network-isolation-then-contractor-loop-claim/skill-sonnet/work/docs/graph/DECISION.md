# Graph decision

Decision: recursive-sql

The question was whether to move the heating network into Neo4j, as a bidding contractor suggests because recursive SQL cannot cope with loops. No: the isolation query already runs as recursive SQL on the SQLite file the register export feeds, at 35 ms p95 on the full network against a 2 s limit (both stated by the user), and its walk keeps only the node id, so `UNION` drops revisited nodes and the ring mains end.

## Workload facts

- The question asked of the connections: from every plant, walk along pipes between nodes (a walk of data-dependent depth) skipping the isolated pipe, then list substations not reached (sql/isolate.sql).
- Loop handling: the recursive CTE `fed(node_id)` carries only the node id and uses `UNION` (not `UNION ALL`), so a node reached again adds no new row and the recursion terminates on rings (sql/isolate.sql, lines 1-2 and the `UNION`).
- Required work: each node enters the walk once, so at most 1,900 nodes are visited, joined through the `pipe_a` and `pipe_b` indexes over 2,400 pipes (derived: sizes stated by the user; indexes in db/schema.sql). The walk is not a row-per-route query.
- Size: about 2,400 pipes, 1,900 nodes and 610 buildings (stated by the user). Average fan-out 2 x 2,400 / 1,900 = about 2.5 pipe ends per node (derived).
- Measured latency: 35 ms p95 on the full network since the rewrite (stated by the user, not re-measured here; no database copy in the repo).
- Latency requirement: under 2 s (stated by the user). 35 ms is about 1.75% of the limit (0.035 / 2).
- Load: about 40 isolations a day by operators (stated by the user); online screen, one request at a time in effect (40 a day is under one every 10 minutes across an 8-hour shift).
- Writes and freshness: the model is a SQLite file `var/heatnet.db`, exported from the asset register whenever the network changes (README.md).
- What is operated today: SQLite, one file, not committed (README.md, .gitignore).
- What was already tried: in March the old version of the query hung on the rings; it was rewritten so the walk keeps only the node id, and has run at 35 ms p95 since (stated by the user). The cause was the walk carrying more than the node id, so each route was a separate row; the fix is in place in sql/isolate.sql.
- Tender context: the contractor's claim that recursive SQL cannot cope with loops is not supported by this query, which handles the rings with `UNION` and has a measurement behind it.
- unknown: growth of the network; the request states no growth rate and the repo has none. Also unknown: the SQLite version in use and the max latency (only p95 was given). Neither changes the verdict at the current margin.

## Options considered

- graph-database (a dedicated graph store, Neo4j as the contractor proposes): rejected, because recursive SQL on the existing SQLite already meets the need at 35 ms p95 against 2 s on a 1,900-node, 2,400-pipe network, and a second store would need a load step for every register export.
- in-process-library (the edges loaded into memory): rejected, because the query in place already meets the need; a library would add a copy of the network to load and keep fresh for no required gain. It would hold, but it is not needed.
- recursive-sql (recursive queries on the SQLite file already run): chosen, because the walk is a data-dependent-depth reachability walk, it handles loops through `UNION` on a node-id-only walk, and it runs at 35 ms p95 against a 2 s limit (stated by the user, with the query in sql/isolate.sql).
- no-graph (plain joins, no traversal): rejected, because the question is reachability from the plants over a path of unknown length, which needs a walk.

## What would change the decision

- Measured p95 on the isolation screen rising past 2 s (the limit stated by the user) at the network's real size, or a network growing to the point that the walk visits far more than today's 1,900 nodes, would move this to in-process-library first, since the edge list would still fit easily in memory; growth to an edge set too large for one process, with SQL measured failing, would be the condition for graph-database.
- A new requirement for whole-network analyses, such as every single-pipe failure computed in one batch, would move this to in-process-library; the control-room owner sets that need.
- A change to the query that makes the walk carry more than the node id (a path, a depth counter, a flow value) would bring back the March problem of one row per route on rings; keep the node-id-only form, or re-measure on the full network.
- A tender requirement that the network live in a graph store for reasons other than this query (shared model with other systems) is a business need for the owner to state; it is not shown here.
