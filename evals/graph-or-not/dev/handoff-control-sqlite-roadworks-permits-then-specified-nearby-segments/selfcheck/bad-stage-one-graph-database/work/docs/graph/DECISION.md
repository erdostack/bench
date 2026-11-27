# Bus operator notices for street works permits

Decision: graph-database

## Workload facts (from the conversation, 2026-11-24)

- About 52,000 segments, 47,000 junctions; weekly refresh; about 400 permits a week; many loops.

## Options considered

- graph-database: rejected; a server for a weekly file.
- in-process-library: would also work.
- recursive-sql: chosen; a depth-capped walk over segments sharing junctions.
- no-graph: no; "near" is more than one step.

## What would change the decision

- Notices on live road closures at a much higher rate.
