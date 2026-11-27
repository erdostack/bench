# 0007. Rate inheritance

Status: Accepted
Date: 2026-11-23

Decision: recursive-sql

Evidence: docs/perf/2026-10-rate-tree-bench.md (48,200 nodes, depth 6, p95 3 ms at 2,400 req/s) and docs/slo.md
(p95 under 50 ms; revisit above half of it).

Rejected: graph database (a second copy of the rates for a read at 6% of its objective); in-memory graph (cache
invalidation on every rate change); no-graph (inheritance depth varies).

Revisit when the effective-rate p95 passes 25 ms in production.
