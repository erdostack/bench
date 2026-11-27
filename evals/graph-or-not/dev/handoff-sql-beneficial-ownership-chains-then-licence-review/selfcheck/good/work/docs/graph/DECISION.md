# Ultimate-owner check

Decision: graph-database

## Workload facts (from the conversation, 2026-11-23)

- 48M companies, 61M holdings; chains up to 24 deep; cross-holdings make cycles.
- Budget: 800 ms p95 (compliance officer waits on the onboarding screen).
- sql/ubo.sql (path array, indexes on both columns): 4.6 s p95 on a replica.
- Closure table: about 2.1 billion rows with cycles; 1.8M holding changes a day. Abandoned.
- networkx on a 5% sample: 3.4 GB, so about 70 GB in total; hosts have 32 GB.

## Options considered

- recursive-sql: measured, 4.6 s against 800 ms.
- in-process-library: does not fit (70 GB vs 32 GB).
- graph-database: chosen.
- no-graph: no.

## What would change the decision

- Postgres meeting 800 ms on the real data, or the graph fitting comfortably in a host's memory.
