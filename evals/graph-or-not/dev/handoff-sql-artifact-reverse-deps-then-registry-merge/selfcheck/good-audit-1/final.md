Still stands: no

The decision (docs/graph/DECISION.md) was in-process networkx under the platform lead's rule: it stays in-process
while the graph fits in half a 32 GB host, 16 GB, and past that it moves to a graph database.

- Edges: 9.2M, then 33M
- Resident memory: 6 GB, then 21 GB
- p95: 38 ms, then 45 ms, against 500 ms

At about 636 bytes per edge the 16 GB line allows about 25.1M edges, so 33M is over it. I've updated the record to
graph-database.
