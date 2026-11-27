Position: keep

We decided against a graph database: see-also stays one query on Postgres (no-graph, nothing is traversed: the page
lists an article's own links and stops). The numbers are in docs/: Ruth's September benchmark gives 2.3 ms p95 at
1,400 req/s with the merged 112,000 articles (1.9 ms today), and the SLO is 150 ms p95 for the page with a review at
75 ms per query. There is no speed to gain.
