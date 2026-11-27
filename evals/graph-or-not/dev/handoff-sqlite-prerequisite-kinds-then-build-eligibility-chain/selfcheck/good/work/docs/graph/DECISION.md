# Prerequisite list on course pages

Decision: recursive-sql

## Workload facts (from the conversation of 2026-11-24)

- What goes on the list (the registrar's rule): **required and concurrent** prerequisites, all the way back.
  **Recommended never counts**, and neither does anything reached only through a recommended one.
- 2,400 courses, 3,900 prerequisite rows, longest chain 7 deep.
- Loops: cross-listed pairs list each other as required; 23 counted, not cleaned up before next year.
- 1.5 MB SQLite file rebuilt every term; about 3,000 course page views a day.

## Options considered

- graph-database (Adaeze's proposal): rejected, a server for a 1.5 MB catalogue.
- recursive-sql: chosen. WITH RECURSIVE over prerequisite, UNION on the course id alone so the loops end.
- in-process-library: fine too at this size; no need.

## What would change the decision

- A catalogue that changes many times a day, or lists needing per-student rules.
