# Tag tree benchmark, October 2026 (Joost)

Query: `sql/tag_articles.sql`, on a production snapshot (prod-replica-2, Postgres 16.4), 30 minutes per run,
replaying tag-page requests from the access log.

| | tags | deepest | articles tagged | request rate | p50 | p95 | p99 |
|---|---|---|---|---|---|---|---|
| today | 6,200 | 7 levels | 2.8M | 900 req/s | 1.1 ms | 4.2 ms | 9.8 ms |
| with regional editions (synthetic regional tags added to the snapshot) | 19,000 | 9 levels | 7.5M | 2,100 req/s | 1.6 ms | 6.8 ms | 15.1 ms |

The regional run adds the nine editions' tag trees as the editors sketched them (each edition mirrors the national
tree under its own root, plus local tags) and replays the access log at the request rate marketing projects.
Plans stay index scans on `tag_parent` and the article_tag primary key in both runs.
