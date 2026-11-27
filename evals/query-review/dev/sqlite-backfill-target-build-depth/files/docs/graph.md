# Dependency graph

- Acyclic: the build tool rejects a dependency cycle before anything reaches this database.
- Libraries are shared heavily: a typical service target reaches the same low-level libraries
  through hundreds of different routes (protobuf, logging, the RPC stack).
- ~9,000 targets, ~44,000 deps rows.
