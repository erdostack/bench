Decision: recursive-sql

Stay on Postgres (there is nothing recursive here; it is a plain join). Recorded in docs/decisions/mutual-connections.md.
7 ms p95 for the intersection against a 100 ms panel budget, 90 views/s, 3.1M connections. Revisit at 50 ms p95, as agreed with Lena.
