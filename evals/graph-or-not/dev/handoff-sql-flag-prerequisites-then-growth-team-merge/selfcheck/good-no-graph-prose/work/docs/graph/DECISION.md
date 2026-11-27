# Flag prerequisites: where the dependency walk lives

Decision: no-graph

## Workload facts (from the owner, 2026-11-23)

- 640 flags, 1,100 prerequisite links; deepest chain 4. The admin UI rejects prerequisites that would make a loop.
- SDKs download one JSON snapshot (1.2 MB) and evaluate locally: 0.08 ms p99.
- Agreed limits (mobile team): snapshot under 5 MB, evaluation under 1 ms p99. If either is crossed, evaluation
  moves to a server-side service.

## Options considered

- graph-database (Bruno's proposal): rejected. A network call per evaluation, or a second store behind a snapshot
  that already holds the whole graph.
- recursive-sql: not where evaluation happens.
- in-process-library: chosen. The snapshot is the graph; the SDK walks prerequisites in memory.
- no-graph: close; the walk is a few steps.

## What would change the decision

- Snapshot at or over 5 MB, or evaluation at or over 1 ms p99: move evaluation server-side.
