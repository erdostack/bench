# Reach panel

Decision: in-process-library

## Workload facts

- 16 families (the Pucci have no ties), 20 marriage ties, never changes; 25 students for a term.

## Options considered

- graph-database (Neo4j): rejected, a server for 20 ties.
- in-process-library: chosen, networkx shortest-path lengths with a cutoff.
- recursive-sql: fine too at this size.

## What would change the decision

- Nothing foreseeable; the data is historical.
