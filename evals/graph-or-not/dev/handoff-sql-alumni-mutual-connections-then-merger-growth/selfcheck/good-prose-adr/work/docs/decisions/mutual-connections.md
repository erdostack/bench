# Mutual connections: where the query lives

Decision: recursive-sql (stay on Postgres; a fixed one-step intersection, no recursion)

Owner's numbers on 2026-11-23: 220k members, 3.1M connections, 90 profile views/s at peak, the panel's share of
the page is 100 ms, the intersection query measured 7 ms p95 on a copy of prod.

Lena proposed Neo4j. Agreed instead: we revisit the moment the query passes 50 ms p95 in production.
