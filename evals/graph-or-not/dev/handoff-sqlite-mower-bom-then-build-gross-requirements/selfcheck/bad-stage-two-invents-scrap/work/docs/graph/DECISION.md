# Gross requirements

Decision: recursive-sql

## Workload facts

- 48,000 items, 210,000 BOM lines, at most 11 levels; about 300 explosions a day, 3 s allowed.
- Recursive query on a copy: 0.4 s.

## Options considered

- graph-database: rejected, a second copy of PLM for a walk Postgres answers.
- recursive-sql: chosen.

## What would change the decision

- The query passing 3 s.
