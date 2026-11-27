# Connections panel on the stop screens

Decision: no-graph

## Workload facts (from the conversation, 2026-11-24)

- Customer services' rule: Connections = every route you can catch at this stop OR at the stop across the road
  (people cross over). Leave out school-only routes.
- Timetable export: about 6,900 stops, 380 routes, 41,000 stop-route rows, rebuilt nightly (SQLite).
- About 1,200 screens refresh once a minute.

## Options considered

- graph-database (Kai): rejected. A second store for a nightly file; the panel needs no traversal.
- in-process-library: not needed.
- recursive-sql: not needed; the pair is one row and the routes one join.
- no-graph: chosen. SQL on the existing export.

## What would change the decision

- A panel that follows routes onward (places reachable with one change), which would be a walk.
