# Supplier section of the product report

Decision: no-graph

## Workload (stated 2026-11-23)

- Compliance (Ines) need tier-1 suppliers only: who delivers the item to us. No sub-suppliers.
- `supplies`: about 600k rows, including some sub-supplier links recorded by purchasing.
- Report generated on demand about 20 times a day; under 10 s is fine.

## Options

- graph-database (Tomas): rejected; no traversal is asked for.
- in-process-library / recursive-sql: not needed for one hop.
- no-graph: chosen; one join (internal/queries/item_suppliers.sql).

## What would change this

- A requirement for deeper tiers: then a bounded recursive query on `supplies`, before any new database.
