Decision: in-process-library. Recorded as docs/adr/0004-connection-panel.md.

Weighted shortest path, length 1 / weight, on 77 characters and 254 ties: networkx in the app (0.1 ms a lookup).
Neo4j would be a server to run for a few hundred lookups a day; Dijkstra does not belong in recursive SQL.
