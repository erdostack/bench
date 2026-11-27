# Rolled-up cost

Decision: recursive-sql

## Workload facts

- 9,000 items, 31,000 BOM lines, up to 7 levels; about 200 quotes a day.
- Foreign keys are not enforced; about 300 lines point at purged items.

## Options considered

- graph-database: rejected. recursive-sql: chosen.

## What would change the decision

- Costing everything on every load.
