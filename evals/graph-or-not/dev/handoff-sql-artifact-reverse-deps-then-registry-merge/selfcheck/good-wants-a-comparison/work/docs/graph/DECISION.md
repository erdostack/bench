# Yank-impact check

Decision: need-more-information

## Workload facts (from the conversation, 2026-11-23)

- MySQL 8: 1.4M artifact versions, 9.2M dependency edges, chains up to 30 deep.
- Budget: 500 ms (the publish CLI waits on the check).
- Loop in impact/reverse.py: 6.1 s p95. WITH RECURSIVE on a replica, on the by_target index: 2.4 s p95.
- networkx in the registry service: 6 GB resident, 38 ms p95, publish events applied as they arrive.
- Hosts: 32 GB. Platform lead's rule: in-process while the graph fits in half a host (16 GB); past that, a graph
  database, not bigger hosts.

## Options considered

- recursive-sql: measured at 2.4 s against 500 ms. Out.
- in-process-library: chosen.
- graph-database: the agreed next step past 16 GB.
- no-graph: no.

## What would change the decision

- The in-process graph passing 16 GB resident (half a host): move to a graph database.

Update: 21 GB resident after the merge, past the 16 GB line. Moving off in-process; need a graph database comparison (load 33M edges, replay the check) before picking one.
