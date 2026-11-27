# 0007. Category subtree for the browse filter

Status: Accepted
Date: 2026-11-23

Decision: recursive-sql

## Workload (stated 2026-11-23)

- 14k categories, at most 9 levels deep.
- Subtree query (sql/category_subtree.sql) 4 ms p95; category filter budget 80 ms end to end; about 700 browse
  requests/s at peak.

## Options

- graph-database (Rhea's proposal): rejected for now; a second store for a query at 5% of its budget.
- in-process-library: rejected; a cache of the tree to invalidate on every catalogue change.
- recursive-sql: chosen; what runs today.
- no-graph: rejected; depth varies.

## What would change this

- Agreed with Rhea: revisit if the subtree query goes past 40 ms p95 in prod (half the 80 ms budget).
