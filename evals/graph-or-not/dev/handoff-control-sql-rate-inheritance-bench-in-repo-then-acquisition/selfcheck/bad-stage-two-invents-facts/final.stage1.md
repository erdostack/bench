Decision: recursive-sql. Written up in docs/graph/DECISION.md.

The benchmark in docs/perf/2026-10-rate-tree-bench.md settles it: 48,200 nodes, at most 6 levels, and the recursive
query runs at 3 ms p95 at the production peak of 2,400 requests a second, about 6% of the 50 ms objective in
docs/slo.md. The walk is upwards, at most six key lookups, which is what Postgres does best. A graph database would
add a second copy of the rates to keep consistent for a read that is already far inside its objective. The SLO doc's
own rule says when to look again: when the read path uses more than half its objective.
