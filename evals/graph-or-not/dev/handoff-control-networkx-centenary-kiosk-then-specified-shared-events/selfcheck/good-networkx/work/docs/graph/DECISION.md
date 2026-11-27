# Kiosk "how is she connected" screen

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- Southern Women study: 18 women, 14 events, 89 attendances; static.
- Raspberry Pi in the foyer; a few hundred visitors over two months; networkx is installed.

## Options considered

- graph-database (designer's Neo4j): rejected; a server for 32 nodes.
- in-process-library: chosen; shortest path on the woman-event graph.
- recursive-sql: would also work on this size.
- no-graph: rejected; chains through events are a path search.

## What would change the decision

- Nothing; the data is historical.
