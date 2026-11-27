# Where the NOC impact walk lives

Decision: graph-database

## Workload facts (stated in the conversation, 2026-11-23)

- Inventory: 1.6M devices, 2.3M links (Postgres). About 3,000 link changes a day; the NOC wants changes visible
  within a minute.
- Impact walk: median 19 hops, up to 41, through rings and meshes.
- NOC budget: 2 s p95.
- Today (impact/walk.py, one query per hop): 11.2 s p95.
- WITH RECURSIVE with a cycle check, on a snapshot: 7.9 s p95; plan already index scans; time spent on paths
  around the rings.
- Closure table: about 9 billion rows with the rings, and 3,000 changes a day to follow. Rejected.
- networkx spike: 2.9 GB for the whole topology, 0.4 s p95 per walk; but four NOC tools need the same graph.

## Options considered

- recursive-sql: measured, 7.9 s against 2 s, with indexes. Out.
- in-process-library: fast enough, but four tools would each hold and update a 2.9 GB copy.
- graph-database: chosen; one shared graph, fed from provisioning's change stream.
- no-graph: no, the walk is the feature.

## What would change the decision

- If only one tool ends up needing the walk, an in-process graph in that service is the cheaper choice.
