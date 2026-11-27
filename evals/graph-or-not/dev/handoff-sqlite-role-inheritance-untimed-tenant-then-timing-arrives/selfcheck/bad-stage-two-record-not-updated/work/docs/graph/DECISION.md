# Role inheritance for the effective-permissions report

Decision: need-more-information

## Workload facts (from the owner, 2026-11-24)

- Report budget: 3 s p95. About 200 runs a day.
- Sanne's rule, both ways: no new datastore while the indexed recursive query in authz/effective.py meets 3 s p95
  on SQLite; if it misses, role inheritance moves to the identity team's graph store, no more SQLite workarounds.
- 39 of 40 tenants: 6 ms p95. The enterprise tenant (about 40x more roles than the next, deeper inheritance) has
  never been timed; its export to the test box keeps failing.

## Options considered

- graph-database (Kofi): only if the enterprise tenant misses 3 s p95.
- recursive-sql: stays if it meets 3 s p95.
- in-process-library, no-graph: not candidates; the walk is needed and the data is in SQLite.

## What would change the decision

- The enterprise timing: under 3 s p95, recursive-sql; over, graph-database.
