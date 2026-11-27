# Downstream-of-valve walk

Decision: in-process-library

## Workload facts (docs/slo.md, docs/perf/2026-09-downstream-bench.md)

- Objective p95 under 1 s; revisit above 600 ms or 6 GB (pod has 8 GB).
- 410k pipes, 380k nodes, walks up to 160 pipes deep.
- Recursive CTE 5.2 s p95; networkx descendants 0.21 s p95, 1.9 GB.

## Options considered

- recursive-sql with more indexes: the plan already uses the index; 5.2 s.
- graph-database: works, but a new server.
- in-process-library: chosen.

## What would change the decision

- The revisit lines in docs/slo.md: p95 above 600 ms or memory above 6 GB.
