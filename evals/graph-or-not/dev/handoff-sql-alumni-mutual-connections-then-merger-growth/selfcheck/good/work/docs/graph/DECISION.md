# Mutual connections on member profiles

Decision: no-graph

## Workload facts (given by the owner, 2026-11-23)

- 220k members, 3.1M connections (stored once per direction).
- Profile views peak at about 90 a second; the mutual-connections panel gets 100 ms of the page.
- Measured: the intersection query (viewer's connections joined with the member's) on a copy of prod, 7 ms p95.

## Options considered

- graph-database (Lena's proposal): rejected for now. A second store kept in sync, for one join at 7 ms.
- in-process-library: rejected. A copy of 3.1M connections in each container.
- recursive-sql: not needed; nothing recurses.
- no-graph: chosen. One intersection query on Postgres.

## What would change the decision

- Agreed with Lena: if the query goes past 50 ms p95 in prod, look at a graph database properly.
