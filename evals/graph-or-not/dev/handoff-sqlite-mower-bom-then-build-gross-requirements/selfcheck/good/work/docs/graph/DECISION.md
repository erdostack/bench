# Gross requirements for works orders

Decision: recursive-sql

## Workload facts (from the planning conversation, 2026-11-24)

- 48,000 items, 210,000 BOM lines in Postgres; deepest BOM 11 levels.
- About 300 explosions a day from the works-order screen; planners accept up to 3 s.
- A recursive query on a copy, biggest ride-on mower: 0.4 s.
- **Scrap rule (planning lead):** add 4% scrap on every BOM line, compounding down the levels. A part three
  levels down is multiplied by 1.04 three times. The schema has no scrap column; this rule lives here.

## Options considered

- graph-database (consultant's suggestion): rejected. A second copy of the PLM data for a walk Postgres answers
  in 0.4 s.
- in-process-library: workable at this size, but nothing to gain over one query.
- recursive-sql: chosen. WITH RECURSIVE over bom_line, quantities multiplied per line with the scrap factor,
  summed per bought-in part.
- no-graph: no, the explosion goes down up to 11 levels.

## What would change the decision

- Explosions run thousands of times per planning run (MRP net change), or the query passes 3 s.
