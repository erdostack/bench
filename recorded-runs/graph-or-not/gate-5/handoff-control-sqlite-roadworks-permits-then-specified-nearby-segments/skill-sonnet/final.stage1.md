Decision: recursive-sql

Stay on the SQLite database you already run and implement `operators_to_notify` with one recursive query from the permit's segment. A graph database is not warranted here.

The numbers it turns on:
- The whole network is about 52,000 segments and 47,000 junctions, so the average junction degree is about 2.2 (2 x 52,000 / 47,000). A walk cannot touch more than the 52,000 segments, whatever "near" means.
- 400 permits a week is at most about 21 million row visits a week (400 x 52,000) in the worst case, which is a small batch load. The network is refreshed weekly, so there is no continuous-write or online-latency pressure.
- `segment_j1` and `segment_j2` already index the junction columns a walk enters by.

Things to get right in the query, since the network has loops:
- Do not use `UNION ALL` without a visited check. A segment reachable by many routes would come back once per route. Carry a depth column, cap the depth, then reduce to `MIN(depth)` per segment before joining `segment_route` and taking `DISTINCT operator`.
- Add an index on `segment_route(segment_id)`; the schema has none.

What I could not find or measure:
- What "near" means (how many segments or junctions out, or what distance). It sets the depth but does not change the decision. If it means only segments touching the works' own junctions, plain joins (no-graph) are enough.
- `var/streets.db` is not in the repo, so I ran nothing: no row counts, plans or timings. Tail fan-out (big roundabouts) and the number of routes per segment are unknown.

I would revisit this if a real run on the full database misses a latency budget you set at your chosen depth (then load the edges in-process), or if the data went continuous and the SQL was measured failing (then a graph database).

The decision is written to docs/graph/DECISION.md. Nothing else in the repo was changed.
