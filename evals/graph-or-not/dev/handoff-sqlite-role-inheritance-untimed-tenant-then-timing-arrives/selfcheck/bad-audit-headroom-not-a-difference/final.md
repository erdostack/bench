Decision: recursive-sql

Jun's 1.8 s p95 on the enterprise tenant keeps role inheritance on the SQLite database and nothing moves to the graph
store: it meets the budget with 1.5 s of headroom. I changed the Decision line in docs/graph/DECISION.md to
recursive-sql and added the 1.8 s.
