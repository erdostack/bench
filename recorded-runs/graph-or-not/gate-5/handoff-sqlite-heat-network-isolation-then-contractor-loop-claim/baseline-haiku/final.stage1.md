Decision: recursive-sql

Don't move the network into Neo4j. The current query already handles the loops, it is well inside the budget, and the contractor's premise that recursive SQL "can't cope with loops" doesn't match what the query does.

Why it works on rings: the recursive CTE in `sql/isolate.sql` uses `UNION`, not `UNION ALL`, and it carries only `node_id`. A node reached a second time produces a row identical to one already in the set, so `UNION` discards it and the walk stops. The set of distinct nodes is bounded by the 1,900 nodes in the network, so the walk cannot run away on a loop. That is the fix you made in March, and it is the standard way to traverse a cyclic graph in SQL.

Why the speed is adequate: you measured 35 ms p95 on the full network. The budget is 2 s and the load is about 40 isolations a day, so the margin is roughly 50x at p95 and the load is trivial. The indexes `pipe_a` and `pipe_b` on `pipe(a_node)` and `pipe(b_node)` support the join from each fed node to its pipes. Two caveats on that number, both worth checking before the tender closes: it should be measured on the production-sized database file with a cold cache, and on the worst-case isolation (a pipe whose removal forces the walk across most of the network), not only a typical one. Even at several times the measured time, it stays far under 2 s.

Why not a graph database: the data is about 2,400 edges and 1,900 nodes, the only query is reachability from plants with one pipe removed, and the existing query already answers it. Adopting Neo4j would add a second datastore to keep in sync with the asset-register export and a new operational dependency in a control room, for no measured benefit. An in-process graph library would also work, but it adds a load-and-cache step and a second source of truth for no gain at this size.

Two things to check in the query itself, neither of which changes the decision:
- `NOT IN (SELECT node_id FROM fed)` is correct here because `node_id` is the primary key and so never NULL. If that ever changed, the NOT IN would silently return no rows.
- The walk seeds from every `kind = 'plant'` node. That is right if all plants feed the network, but if a plant can be isolated on its own it should be modelled separately.

Revisit the decision only if isolation needs multi-hop questions the current query can't express, or if measured p95 on the production file goes above roughly 500 ms.
