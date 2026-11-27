Still stands: yes

We chose the graph database because nothing cheaper met the 1.5 s p95 storm budget (docs/graph/DECISION.md).
Postgres was 8.4 s then and is 4.9 s now: better, still more than three times over. In memory the grid was
estimated at about 35 GB (2.1 GB for 6% of it), so 32 GB servers still don't hold it, and 16 GB was the old size.
Splitting by region is no way round it either, since 41% of storm traces cross regions. Going back would mean
missing the budget in every storm.
