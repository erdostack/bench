# Nested list expansion

Decision: recursive-sql

## Workload facts (from the owner, 2026-11-23)

- 2,300 lists, 41k member rows, on the relay's SQLite copy of the list config.
- Nesting goes 14 levels deep (all-company, divisions, departments, teams ...).
- 37 loops right now (lists that include each other through others).
- sql/expand.sql carries the path of lists entered and never enters one twice: 3 ms p95; delivery allows 500 ms.
- About 90k messages a day go to lists.

## Options considered

- graph-database (Pia's proposal): rejected. A server next to the relay for a walk that takes 3 ms.
- in-process-library: no need.
- recursive-sql: chosen. Keep sql/expand.sql as it is; the path guard is what ends the loops.
- no-graph: no; nested lists are a walk.

## What would change the decision

- Expansion nearing the 500 ms delivery budget.
- Anyone removing the path guard: with loops in the data the walk would no longer end on its own.
