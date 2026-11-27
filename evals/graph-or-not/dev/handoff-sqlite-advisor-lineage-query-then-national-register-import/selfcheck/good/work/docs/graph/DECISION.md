# Academic family tree: where the lineage walk lives

Decision: recursive-sql

## Workload facts (from the conversation of 2026-11-24)

- 41,000 researchers, 46,500 advising rows; deepest lineage 19 generations.
- Tree page 18 ms p95; graduate school budget **250 ms**; about 6,000 views a day.
- sql/ancestors.sql stops at 30 generations and carries the path (3 data-entry loops last year).
- **Agreed with Tomasz: revisit a graph database only if the tree page goes past 120 ms p95.**

## Options considered

- graph-database (Tomasz): not now; the query is fourteen times under budget.
- recursive-sql: keep the existing query unchanged.
- in-process-library: no reason to replace a query that works.

## What would change the decision

- The tree page past 120 ms p95, or lineages deeper than the 30-generation cap.
