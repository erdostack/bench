Position: keep

Thanks for the review. The ring-main case is the one we already hit, and it is fixed in the query we run today.

What we decided (docs/graph/DECISION.md): keep the isolation screen on recursive SQL on the SQLite file the register export feeds. Neo4j is not needed.

Why the "loops forever" claim doesn't apply:
- In March the old version of the query did hang on the rings. The cause was the query, not SQL. It carried more than the node id, so every route around a ring was its own row.
- The current query (sql/isolate.sql) walks with `fed(node_id)` and keeps only the node id. It uses `UNION`, not `UNION ALL`, so a node reached a second time adds no row and the recursion ends on rings. Each node enters the walk once.
- I ran it on a synthetic network of about 1,900 nodes and 2,170 pipes, a full ring plus chords that make many cycles. It finished in about 9 ms. That is a stand-in, not our real network.

The numbers:
- Network: about 2,400 pipes, 1,900 nodes and 610 buildings. The walk visits at most 1,900 nodes.
- Isolation screen: 35 ms p95 on the full network since the rewrite, against a 2 s limit. That is about 1.75% of the limit (0.035 / 2).
- Load: about 40 isolations a day, which is fewer than one every 10 minutes.

A graph database would add a second store and a load step after every register export, to fix a problem we no longer have.

Two things would reopen it: p95 past 2 s on the real network (or the network growing far past today's size), or someone changing the query so the walk carries more than the node id, such as a path or a depth counter. That change would bring the March problem back, so keep the node-id-only form or re-measure first.

I did not re-measure on the real network because there is no copy of `var/heatnet.db` in the repo, so the 35 ms is your figure. Nothing in the repo was changed.
