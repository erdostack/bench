Decision: recursive-sql

Do not move the network into Neo4j. The existing recursive query in `sql/isolate.sql` already handles the ring mains: `UNION` over the node id alone keeps each node once, so the walk ends on loops. The stated p95 of 35 ms is far inside the 2 s budget, at about 40 isolations a day.

Numbers the decision turns on:
- Present p95: 35 ms on the full network (your figure; I could not check it, because `var/heatnet.db` is not in the repo).
- My synthetic check, at the same size (1,900 nodes, 2,400 pipes, every pipe isolated once, two topologies): p95 of 29 to 33 ms, max about 62 ms, and every walk reached all 1,900 nodes. The plan uses the `pipe_a` and `pipe_b` indexes, with no full scan of `pipe`.
- Load: 40 isolations a day x 35 ms is about 1.4 s of query time per day.

What I could not find or measure: the real network's topology and degree tail, the timing on the real file under production load, and how often the network is re-exported. The owner of the 2 s budget is not named in the request.

What would change this: a p95 above 2 s on the real file (check the plan and indexes first), a jump to many isolations per second online, or a need to run every pipe's isolation as one batch. The batch case would point to an in-process library on a snapshot. A graph database would be considered only if SQL were measured failing after those remedies.

The contractor's claim that recursive SQL cannot cope with loops does not hold for this query. Nothing in the repo was changed. The decision record is at `docs/graph/DECISION.md`, and the synthetic benchmark folder was removed.
