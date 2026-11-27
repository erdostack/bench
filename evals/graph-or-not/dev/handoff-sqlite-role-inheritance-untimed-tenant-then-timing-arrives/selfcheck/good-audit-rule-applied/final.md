Decision: recursive-sql

Jun's 1.8 s p95 on the enterprise tenant is under the 3 s p95 budget, so role inheritance stays on the SQLite database and nothing moves to the graph store. It meets the budget with 1.2 s of headroom.

A p95 over 3 s would move this to graph-database. I changed the Decision line in docs/graph/DECISION.md to recursive-sql and added the 1.8 s.
