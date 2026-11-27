# ADR 0012: connection line

Decision: graph-database

History: until the depth was settled we stayed on Postgres (recursive-sql) and asked for the depth.

- 31M members, 1.9B friendships, 4,500 new friendships/s; 2,400 profile views/s; 120 ms budget.
- Depth settled: exact distance up to 4. Measured 4-step query on a replica under peak: 870 ms p95, lag 40 s.
- In-process is ruled out by the 2025-06 incident review.
