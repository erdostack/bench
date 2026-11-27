# "Blocked by" panel

Decision: recursive-sql

## Workload facts (given by the owner, 2026-11-23)

- 2.4M tickets, 900k blocking links; about 1,700 loops in the data right now (mutual blocks and longer rings).
- The panel loads about 40 times a second at peak and has 300 ms.
- Incident last quarter: the old query had no loop guard; a ticket in a loop ran it to the 30 s statement timeout
  and about 40 such queries piled up and took the database down.
- Fixed in October (Lukas): the recursion carries the path and skips tickets already on it
  (src/panels/blockers.sql). Since then: 11 ms p95.

## Options considered

- graph-database (Jonas's proposal): rejected. The incident was the missing loop guard, now fixed; a graph store
  would add a synchronised copy of the links for a query at 11 ms of 300 ms.
- in-process-library: rejected. 900k links copied into every API process.
- recursive-sql: chosen. Keep src/panels/blockers.sql with its path guard.
- no-graph: rejected. Blockers are transitive.

## What would change the decision

- The panel missing its 300 ms with the guarded query.
