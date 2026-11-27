# Circles page

Decision: in-process-library

## Workload facts (from the owner, 2026-11-24)

- 18 women, 14 events, 89 attendances; the study's data never changes. A few dozen visitors a week, shared host.

## Options considered

- graph-database (board member): rejected; a server for 32 nodes.
- in-process-library: chosen; networkx breadth-first search from the chosen woman.
- no-graph: also fine for data this small, but the page is a walk.

## What would change the decision

- Nothing plausible for a fixed historical dataset.
