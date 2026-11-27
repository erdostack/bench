# Rate tree benchmark, October 2026

Production snapshot restored on the staging replica.

- `rate_node`: 48,200 nodes (brand -> region -> hotel -> room type, with optional sub-regions); deepest path 6.
- `rate`: 2.9M rows.
- `effective_rate.sql`, 200k random (room type, date) pairs replayed at the production peak of 2,400 requests/s:
  p50 1.1 ms, p95 3 ms, p99 7 ms.
- Plan: index scan on `rate_node_pkey` per level, then `rate_node_date` on `rate`.

Conclusion: the read path uses about 6% of its 50 ms objective at peak.
