Position: keep

We decided to stay on Postgres (ADR 0009 records it as recursive-sql, though the query is a plain lookup). From docs/: 38,400 articles today, 112,000 after the merge; the see-also query is
2.3 ms p95 at 1,400 req/s on the merged set; the page objective is 150 ms p95. A graph database can't make a 2 ms
lookup meaningfully faster.
