# ADR 0009: outage trace on a graph database

Decision: graph-database

## Workload facts (from the conversation, 2026-11-24)

- 2.9M nodes, 3.4M conductor segments, meshed through normally-open points; about 45,000 switching changes a day.
- Storm load: about 900 traces an hour. Budget: 1.5 s p95.
- Recursive query (path array, indexes on both ends): 8.4 s p95 on the January storm replay.
- networkx: 2.1 GB for one region (6%), so about 35 GB for the grid; trace servers have 16 GB.
- Per-region split: 41% of storm traces cross regions after switching.
- Closure table: 6.8 billion rows, invalidated by switching.

## Options considered

- recursive-sql: measured, 8.4 s p95 against 1.5 s.
- in-process-library: about 35 GB against 16 GB servers; partitioning fails (41%).
- graph-database: chosen; the switching feed updates it as states change.
- no-graph: no; the trace is a variable-depth walk.

## What would change the decision

- Postgres meeting 1.5 s p95 on a storm replay, or trace servers with comfortably more memory than ~35 GB.
