# See-also query benchmark (Ruth, 2026-09-18)

Setup: production snapshot restored on a staging replica (same instance class as production), the query in
`sql/see_also.sql`, article ids replayed from one day of access logs.

Data at the time: 38,400 articles, 211,000 see-also links. With the second product's articles (the merge plan):
about 112,000 articles and 590,000 links, loaded into a second staging copy.

| Data set | Load | p50 | p95 | p99 |
|---|---|---|---|---|
| current (38,400 articles) | 650 req/s (today's peak) | 0.6 ms | 1.9 ms | 3.4 ms |
| after merge (112,000 articles) | 1,400 req/s (expected peak) | 0.7 ms | 2.3 ms | 4.1 ms |

The plan uses the primary key on `article_link` in both cases. The page renders at most 6 links and never follows a
link's own links.
