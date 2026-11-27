# Tag hierarchy: stay on Postgres

Decision: recursive-sql

## Workload facts (from docs/, checked 2026-11-23)

- docs/perf/2026-10-tag-tree-bench.md: today 6,200 tags, 7 levels, 4.2 ms p95 at 900 req/s. With the regional
  editions (synthetic): 19,000 tags, 9 levels, 6.8 ms p95 at 2,100 req/s. Plans are index scans in both.
- docs/slo.md: tag page 250 ms p95; review when a single query passes 120 ms p95.

## Options considered

- graph-database (Sanne's proposal): rejected. The projected query is 6.8 ms against a 120 ms review line.
- in-process-library: not needed.
- recursive-sql: chosen. Keep sql/tag_articles.sql.
- no-graph: no; sub-tags are a tree walk.

## What would change the decision

- The tag query approaching 120 ms p95.
