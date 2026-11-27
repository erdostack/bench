Decision: graph-database. Written up in docs/graph/DECISION.md.

Every cheaper rung has been measured and misses: the recursive query is 4.6 s p95 with indexes against an 800 ms
budget, a closure table would be 2.1 billion rows under 1.8M changes a day, and the whole graph in networkx would
be about 70 GB on 32 GB hosts. Chains up to 24 deep with cycles over 61M holdings is a graph database's workload.
