# Marriages-apart widget

Decision: in-process-library

## Workload facts

- 16 families (Pucci with no marriages), 20 marriages, never changes; a couple of hundred views a day.

## Options considered

- graph-database (Neo4j): rejected, a server for 20 edges.
- in-process-library: chosen, networkx shortest_path_length.
- recursive-sql: fine too at this size.

## What would change the decision

- Nothing foreseeable; the data is historical.
