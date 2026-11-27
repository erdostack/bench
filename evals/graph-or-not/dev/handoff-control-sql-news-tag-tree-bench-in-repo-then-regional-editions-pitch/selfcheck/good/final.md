Position: keep

Sanne, we looked at this against the numbers in docs/. Joost's October benchmark has the tag query at 4.2 ms p95 today
(6,200 tags, 900 req/s) and 6.8 ms p95 with the regional editions added (19,000 tags, 9 levels, 2,100 req/s). The tag
page's objective is 250 ms and the review line for a single query is 120 ms. So we decided to keep the recursive
query on Postgres: there is no slowness for a graph database to fix, and it would add a second copy of the taxonomy.
