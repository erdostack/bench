# Role inheritance: where it lives

Decision: recursive-sql (provisional until the enterprise tenant is timed)

Budget 3 s p95, ~200 runs/day. Rule (Sanne): no new datastore while the indexed recursive query meets 3 s; if it
misses, the identity team's graph store. Small tenants 6 ms p95. Enterprise tenant: never timed.
