# Rolled-up cost on the quote page

Decision: recursive-sql

## Workload facts (from the conversation of 2026-11-24)

- 9,000 items, 31,000 BOM lines, BOMs up to 7 levels; about 200 quotes a day; SQLite file loaded from the ERP export.
- About 300 BOM lines point at items purged from the item table. SQLite does not enforce the REFERENCES
  (foreign keys are off unless `PRAGMA foreign_keys = ON` is set per connection, and quotecalc/db.py does not).
- **Finance's rule: if anything anywhere under an assembly is missing from the item table, the assembly has no
  cost at all (the quote page shows it as incomplete). Never a partial total.**

## Options considered

- graph-database (Piotr): rejected. It does not fix the purged rows; the loader or a check does.
- in-process-library: workable at this size.
- recursive-sql: chosen. One recursive query that carries the cost and a "missing" flag up the BOM.
- no-graph: no, the rollup goes down up to 7 levels.

## What would change the decision

- Costing every item on every ERP load (thousands of rollups at once): then cost the whole BOM in one pass.
