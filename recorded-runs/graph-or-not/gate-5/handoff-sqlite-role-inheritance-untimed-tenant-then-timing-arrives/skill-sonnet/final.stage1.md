Decision: need-more-information

Sanne's rule turns on one number that nobody has: the time of the effective-permissions query on the enterprise tenant. The 6 ms p95 is from the 39 small tenants, and the enterprise tenant has about 40 times more roles and much deeper inheritance, so it cannot be scaled up from that. Two different values of the missing number lead to different options.

Questions, with how to get each and which way it points:
1. What is the p95 of `effective_permissions` on the enterprise tenant? Run it for a sample of its users, including those holding the most and the deepest roles. If the test-box export keeps failing, run it read-only against the production file, or send counts instead: rows in `role`, `role_inherits` and `user_role` for that tenant, and the longest inheritance chain. At or under 3 s the answer is recursive-sql and you change nothing. Over 3 s, Sanne's rule sends it to the identity team's graph store.
2. How many rows does the walk produce for the deepest enterprise roles compared with the number of distinct roles reached? The query uses `UNION ALL` with a path string, so it returns one row per route. If the miss is only route repetition, Sanne needs to say whether a deduplicating rewrite counts as one of the "SQLite workarounds" the rule rules out.

What I found: the report runs about 200 times a day (about 0.002 per second), so load is not the issue, only the enterprise tenant's size and depth. The query enters the walk through primary-key indexes on both `role_inherits` and `user_role`, so missing indexes are not the likely problem.

I could not find: any timing or data for the enterprise tenant (no database file is in the repo), its role and edge counts, or the SQLite version. I measured nothing. I wrote `docs/graph/DECISION.md` with the facts and conditions. Nothing else in the repo was changed.
