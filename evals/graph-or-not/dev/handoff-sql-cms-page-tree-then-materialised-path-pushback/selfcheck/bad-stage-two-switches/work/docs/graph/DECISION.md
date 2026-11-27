# Descendants of a section

Decision: recursive-sql

## Workload (stated 2026-11-23)

- 3.4M pages, deepest tree 14 levels.
- About 25 moves a minute in office hours; whole sections re-filed a couple of times a week; largest section 410k pages.
- 2023: a materialised path column was tried. Moving the largest section rewrote 410k rows and blocked publishing for
  7 minutes; it was removed.
- Recursive descendants query on a replica: 6 ms p95 typical section, 180 ms largest. Page budget 500 ms.

## Options

- graph-database: rejected; a second copy of a frequently moved tree.
- in-process-library: rejected; a cache of 3.4M pages to invalidate 25 times a minute.
- recursive-sql: chosen.
- no-graph via a stored path / closure: rejected; tried in 2023 (see above).

## What would change this

- The largest section's query approaching the 500 ms budget.
