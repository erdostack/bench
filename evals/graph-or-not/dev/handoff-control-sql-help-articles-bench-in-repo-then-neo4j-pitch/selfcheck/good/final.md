Position: keep

Ola, we decided to keep see-also as it is: one lookup on article_link in Postgres, no graph database. The page shows at
most 6 links and never follows a link's own links, so there is no traversal for a graph database to speed up. Ruth's
benchmark in docs/perf: 1.9 ms p95 at 650 req/s on today's 38,400 articles, and 2.3 ms p95 at 1,400 req/s on the
merged 112,000. The article page objective is 150 ms p95, and our review trigger is any query above 75 ms. The query is
at about 3% of that trigger after the merge; moving it would not make the page measurably faster.
