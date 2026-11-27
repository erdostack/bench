Decision: recursive-sql

No, do not move the network to Neo4j on the strength of the contractor's claim. The isolation query in sql/isolate.sql is already recursive SQL on your SQLite file, and the rings are not the problem it was in March. The walk carries only the node id and uses UNION, which drops any node reached a second time, so loops end. That is the rewrite you made.

Numbers it turns on:
- 35 ms p95 on the full network against the 2 s limit, about 1.75% of the budget (both your figures; I had no database copy and did not re-measure).
- The walk visits each node once, so at most 1,900 nodes over 2,400 pipes, using the existing pipe_a and pipe_b indexes.
- About 40 isolations a day, with the model re-exported from the asset register whenever the network changes. A graph store would add a second engine and a load step for every export.

What I could not find: network growth rate, the SQLite version, and maximum (not just p95) latency. None of these changes the answer at this margin.

For the tender: keep the node-id-only form of the walk as a stated requirement. If someone adds a path, depth or flow column to the walk, it will go back to one row per route on rings, as it did in March. The conditions that would reopen this are written in docs/graph/DECISION.md under "What would change the decision".

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
