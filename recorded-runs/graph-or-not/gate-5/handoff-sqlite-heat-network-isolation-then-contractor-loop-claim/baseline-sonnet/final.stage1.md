Decision: recursive-sql

No, don't move to Neo4j for this. The contractor's premise is wrong for the query you have now.

- **Loops are handled.** `sql/isolate.sql` uses `UNION` (not `UNION ALL`) and the walk carries only `node_id`. A node that is reached a second time is dropped, so the walk stops at ring mains. The March hang came from carrying path or distance columns, which made every row distinct. You already fixed that. Recursive SQL can cope with loops when the query is written this way.
- **The numbers have a lot of headroom.** 35 ms p95 on the full network (about 1,900 nodes and 2,400 pipes) against a 2 s budget is roughly 50 times faster than needed. About 40 isolations a day is negligible load.
- **The indexes are in place.** `pipe_a` and `pipe_b` cover the join in each direction.
- **The data is exported from the asset register into SQLite whenever the network changes.** Neo4j would add a second datastore, a sync job after every export, a new thing to operate, and a new query language. All of that buys nothing here.
- **An in-memory graph library** would also work at this size, but it has the same answer and more moving parts than the query you already have, so it isn't worth switching.

I read the query and schema but didn't run it. The 35 ms figure is yours, and I haven't re-measured it.

What I'd put in the tender instead of a database migration:
- Keep the requirement as an outcome: the screen answers in under 2 s on the full network, including ring mains. Don't specify a technology.
- Ask bidders to show a measured result on your full network, not a claim that a technology is needed.
- Add a regression test with a ring (a loop of pipes with a substation on it) so nobody reintroduces a path-carrying walk. Add a second test where isolating one pipe on a ring should cut off nobody, since the other way round the ring still feeds it.

Things that would change this decision, none of which are in the evidence you gave me:
- Questions that need more than reachability, such as the cheapest or hydraulically valid re-route, or pressure and flow simulation.
- Growth by a couple of orders of magnitude, or many concurrent users.
- A requirement for multi-hop analysis across asset types that the SQL starts to make painful.

If any of those are on the roadmap, say so and I'll look again.

One thing I noticed in the query. A building that is only reachable through the isolated pipe, and whose plant feed is cut elsewhere too, is correctly listed. A substation that is fed from two directions is correctly not listed. The query treats every pipe as usable in both directions and ignores valves and flow direction. That is fine if the model is as the schema describes, but check it matches how operators actually isolate, because it would matter more than the database choice.
