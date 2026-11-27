# Service level objectives: public site

| Surface | Objective | Review threshold |
|---|---|---|
| Article page | 300 ms p95 (server) | any single query over 100 ms p95 |
| Tag page | 250 ms p95 (server) | any single query over 120 ms p95 |
| Search | 400 ms p95 | n/a |

A query crossing its review threshold gets a design review before the next release.
