# See-also links

Decision: no-graph

## Workload facts (from docs/perf/2026-09-see-also-bench.md and docs/slo.md)

- One lookup per page view, at most 6 links, never follows a link's own links.
- Today: 38,400 articles, 211,000 links; 1.9 ms p95 at 650 req/s.
- After the merge: about 112,000 articles, 590,000 links; 2.3 ms p95 at 1,400 req/s.
- Article page objective 150 ms p95; review if a single query passes 75 ms p95 for a week.

## Options considered

- graph-database (Ola): rejected; a second store for a primary-key lookup.
- in-process-library, recursive-sql: not needed.
- no-graph: chosen.

## What would change the decision

- The see-also query passing 75 ms p95, or the page starting to follow links of links.
