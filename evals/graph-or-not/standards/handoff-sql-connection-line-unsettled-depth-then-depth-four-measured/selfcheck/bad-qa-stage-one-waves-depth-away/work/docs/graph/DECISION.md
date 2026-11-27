# "How you're connected" line

Decision: graph-database

Earlier: need-more-information (depth unsettled). Settled on Thursday: exact distance up to 4.

## Workload facts (from the owner)

- 31 million members, 1.9 billion friendships (stored once per pair), about 4,500 new friendships a second at peak.
- Profile views peak at 2,400 a second; the line gets 120 ms of the page.
- Depth not settled: PM wants 2 steps, growth wants the exact number up to 4. Decided on Thursday.
- In-memory in our own processes is ruled out (docs/incidents/2025-06-friend-graph-cache.md, platform review).

## Measured (Kemal, replica, replayed peak)

- 4-step query (two steps from each side, intersect): p95 870 ms against the 120 ms budget; replica lag 40 s.

## Options considered

- recursive-sql (Kemal): fine for 2 steps; unproven for 4 at this size and rate.
- graph-database (Ines): justified only if 4 steps is needed and Postgres misses the budget.
- in-process-library: ruled out by the platform review.
- no-graph: no; even 2 steps crosses knows twice.

## What would change the decision

- Depth 2: stay on Postgres (recursive-sql). Depth 4: measure the 4-step query on a replica under peak load;
  over 120 ms means graph-database.
