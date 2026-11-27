Decision: recursive-sql

The rule recorded in docs/graph/DECISION.md decides it: stay on SQLite while the indexed recursive query meets the
report's 3 s p95 budget. The enterprise tenant was the one number missing; it is 1.8 s p95 (budget 3 s), so the
query meets it and role inheritance stays in rolebook. The small tenants were 6 ms. I changed the Decision line in
docs/graph/DECISION.md to recursive-sql and added the 1.8 s measurement.
