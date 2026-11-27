Still stands: yes

The graph database call stands. The best figure on the storm replay is now 4.9 s p95 (was 8.4 s), still about 3.3 times the 1.5 s budget, and the in-memory copy is about 35 GB against the 32 GB trace servers (was 16 GB), so it still does not fit before headroom.

Old and new numbers:
- Storm replay p95: 8.4 s before (path-array query, PostgreSQL version unknown); 4.9 s now (the DBA's CYCLE rewrite on PostgreSQL 17, as you reported). Budget: 1.5 s.
- Trace server memory: 16 GB before; 32 GB now.
- Whole-grid in-memory copy: about 35 GB, extrapolated from 2.1 GB for 6% of the network. That was 2.19 times the old 16 GB limit; it is 1.09 times the new 32 GB limit, so it still does not fit.

Why the CYCLE rewrite does not reopen the decision: it stops loops but still returns one row per route, so it is not the node-only UNION rewrite that the decision asks you to trial. The rewrite is also not in the checkout, which still holds the path-array version, so I have not checked its plan.

The gate before any spend is unchanged: run the node-only UNION rewrite on the January replay on PostgreSQL 17, with EXPLAIN (ANALYZE, BUFFERS) and the distinct count beside the row count. If it meets 1.5 s p95, the decision goes to recursive SQL. If it does not, the next test is the full edge set in the candidate graph database under the real query mix.

Updated: `docs/graph/DECISION.md`, with the new numbers beside the old ones. Nothing else in the repo was changed.
