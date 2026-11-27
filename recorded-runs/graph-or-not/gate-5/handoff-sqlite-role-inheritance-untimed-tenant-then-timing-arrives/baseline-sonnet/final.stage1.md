Decision: need-more-information

Sanne's rule turns on one number you don't have yet: the query's p95 on the enterprise tenant. Without it, the evidence doesn't decide between staying on SQLite and moving to the identity team's graph store.

What the evidence says:
- The 6 ms p95 comes from the 39 small tenants. It tells you nothing about a tenant with about 40 times more roles and much deeper inheritance.
- The query in `authz/effective.py` is a recursive CTE that carries a `path` string per row and skips a role only if it already appears in that row's own path. It does not keep one global visited set. So it enumerates every distinct inheritance path, not every distinct role. Its cost depends on how many paths there are, not on how many roles there are.
- That makes the enterprise tenant's shape matter more than its size. A deep, mostly tree-like hierarchy will be cheap. A deep hierarchy with many roles inheriting from several parents (diamonds) can blow up.

I did a rough check with synthetic data in an in-memory SQLite database, using the real schema and the real query. It is not your data. Each case is a layered role hierarchy, with the user holding one bottom-layer role and each role inheriting from `fan` random roles in the layer above:
- 2,000 roles, 12 layers, 2 parents each: 0.014 s.
- 2,000 roles, 16 layers, 2 parents each: 0.46 s.
- 2,000 roles, 12 layers, 3 parents each: 3.9 s.
So the same query goes from milliseconds to over your 3 s budget, depending only on depth and how many parents each role has. Those timings are from this sandbox and say nothing about your hardware. They show that the answer could land on either side of 3 s, so I can't call it from the small-tenant number.

What would decide it, in order of cheapness:
1. Time the query on the enterprise tenant without exporting it. Run it on the production host against a read-only connection, or on a replica, for a handful of users: the ones with the most roles and the deepest chains.
2. Count the paths without running the full query. Query the enterprise tenant's `role_inherits` for the number of roles, the maximum depth, and the number of roles with more than one parent. Many multi-parent roles on a deep chain is the danger sign.
3. Fix the export. The failing export is what is blocking the measurement, and it may only need `sqlite3 var/authz.db ".backup ..."` or a tenant-filtered copy of the five tables.

How to read the result against Sanne's rule:
- If p95 on the enterprise tenant is under 3 s, stay on SQLite. The rule says no new datastore. Recursive SQL is then the decision.
- If it is over 3 s, the rule says move role inheritance to the graph store. One thing to raise with Sanne before doing so: the current query's cost comes from the per-path `path` string, and swapping that for a plain visited-set recursion (`UNION` instead of `UNION ALL`, no path) is a query fix, not a new datastore. Whether that counts as one of the "SQLite workarounds" the rule forbids is Sanne's call, not mine, so I would ask before changing it.

I did not change any code in the repo.
