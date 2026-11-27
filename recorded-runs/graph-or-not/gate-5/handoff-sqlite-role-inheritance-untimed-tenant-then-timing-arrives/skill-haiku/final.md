Decision: recursive-sql

The decision is now recursive-sql, not need-more-information. Jun's enterprise-tenant timing of the effective-permissions query, 1.8 s p95 over 500 runs with indexes in place, is under Sanne's 3 s p95 budget, so the role-inheritance walk stays on the SQLite database and nothing moves to the graph store. The margin is about 1.67 times (3 s / 1.8 s).

Open points before this is treated as settled:
- Which users Jun timed. If the 500 runs covered only light users, the heaviest user is the one to time, on a read-only copy of the enterprise data with statistics. A p95 over 3 s there would move this to graph-database.
- Whether the test box holds a full copy of the enterprise data, and the plan on that file after ANALYZE (EXPLAIN QUERY PLAN with a real user id).
- Whether 1.8 s against 3 s is acceptable on the enterprise tenant is Sanne's call; the repo sets no margin.

The record is updated in docs/graph/DECISION.md: the Decision line, the facts, and the options now carry the new figure, with the previous values noted. Nothing else in the repository was changed.
