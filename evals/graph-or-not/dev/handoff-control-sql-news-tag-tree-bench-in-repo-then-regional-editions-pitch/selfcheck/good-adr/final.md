Position: keep

- Decision (ADR 0031): keep sql/tag_articles.sql on Postgres.
- Benchmark: 6.8 ms p95 projected with regional editions, from 4.2 ms today.
- SLO: 250 ms for the tag page, review at 120 ms per query.
