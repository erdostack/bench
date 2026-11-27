# Graph decision

Decision: recursive-sql

Kofi asks whether role inheritance for the admin console's effective-permissions report (`authz/effective.py`) should move out of rolebook's SQLite database into the identity team's graph store, under Sanne's rule: no new datastore if the indexed recursive query meets the 3 s p95 budget on SQLite. The record was `need-more-information` because the enterprise tenant had never been timed; Jun has now timed it at 1.8 s p95 over 500 runs with indexes in place, which meets the budget, so the walk stays on SQLite and nothing is moved. The finding it turns on: 1.8 s p95 against 3 s, a margin of about 1.67 times, on the indexed recursive query.

## Workload facts

- Enterprise tenant, p95 on the effective-permissions query: 1.8 s over 500 runs, indexes in place, on the test box (stated by the user, Jun's timing). Previously recorded as unknown. Not stated: which users were timed (the heaviest user or a mix), and whether the test box holds a full copy of the enterprise data with statistics.
- Budget: 3 s p95 (stated by the user; Sanne's rule in the prior record). Margin: 3 s / 1.8 s = 1.67 times (derived).
- Small tenants: 6 ms p95 across the 39 small tenants (stated by the user; prior record). Previously recorded the same.
- 40 tenants share one SQLite database, `var/authz.db` (`README.md`; `.gitignore` excludes `*.db`, so no copy is in the checkout).
- The report query is a `WITH RECURSIVE` walk from a user's roles through `role_inherits`, carrying a comma-delimited `path` string and `UNION ALL`, with the cycle check `instr(held.path, ...) = 0`, and a final `SELECT DISTINCT` over `role_permission` (`authz/effective.py`). Each route is a row, so a role reached by several inheritance paths appears once per path before the `DISTINCT` (the query's structure, not a measured count).
- Indexes that the walk uses: the primary key `(role_id, permission)` on `role_permission`, the primary key `(role_id, parent_role_id)` on `role_inherits`, and the primary key `(user_id, role_id)` on `user_role` (`db/schema.sql`). The separate `role_inherits_parent` index is not the one the walk enters by.
- Plan on an empty schema (no statistics, SQLite 3.53.1, Python `sqlite3`, from the prior record): the walk enters `role_inherits` by the primary key (`SEARCH ri USING COVERING INDEX sqlite_autoindex_role_inherits_1 (role_id=?)`), and the final join reads `role_permission` with `SCAN rp`. This is an empty-schema plan and says nothing about the real planner's choice; the plan on the test box after `ANALYZE` was not reported.
- Runs: about 200 a day, an admin report (stated by the user; prior record). 200 / 86,400 s is about 0.0023 per second, so average load is low; the p95 matters for the single run, not for concurrency.
- Enterprise tenant: about 40 times the roles of the next biggest tenant, and inheritance deeper (stated by the user; prior record). The enterprise role count is unknown (sum: 40 × the next biggest tenant's count, which is unknown).
- Prior naive estimate, now superseded: 40 × 6 ms = 240 ms from roles alone. Not a valid estimate; the measured 1.8 s is the figure that counts.
- unknown: the enterprise tenant's role count, inheritance depth, and the count of routes (rows before `DISTINCT`) for its heaviest user.
- unknown: the role count and inheritance depth of the next biggest tenant (the "40 times" figure is the only ratio given).
- unknown: which users the 500 runs used, and whether the timed copy is a read-only copy of the enterprise tenant, as the prior record's protocol asked.
- unknown: whether the planner on the real file keeps `SCAN rp` (needs `ANALYZE` and `EXPLAIN QUERY PLAN` on that file).
- Looked in: `README.md`, `db/schema.sql`, `authz/effective.py`, `authz/grants.py`, `.gitignore`, `docs/graph/DECISION.md`. No `docs/graph/CONTEXT.md` and no database file in the checkout.

## Options considered

- graph-database (the identity team's graph store): rejected, because Sanne's rule moves role inheritance there only if the query misses 3 s, and the enterprise tenant's measured p95 is 1.8 s. Previously rejected for now, when the enterprise time was unknown.
- in-process-library (the edges loaded into memory): rejected, because Sanne's rule names only the graph store or the existing indexed query, and no size is measured for the whole database, so no copy-per-process figure exists to judge it.
- recursive-sql (the indexed recursive query on SQLite): chosen, because the enterprise p95 of 1.8 s is under the 3 s budget and the small tenants run at 6 ms. The figure is one timing set on the test box; its user mix is the open question below.
- no-graph (plain joins, no traversal): rejected, because inheritance is a walk of data-dependent depth from each user's roles.

## What would change the decision

- The p95 of the report query for the heaviest enterprise user, on a read-only copy of the enterprise data with statistics, over at least 200 timed runs, exceeding 3 s would move this to graph-database under Sanne's rule. Jun's 1.8 s is the decision's basis, and if it covered only light users the heaviest user's time is the one to measure.
- The same measurement on the production read-only replica, if one exists, showing a p95 over 3 s would move this to graph-database.
- A plan showing `SCAN` of `role_permission` at enterprise scale after `ANALYZE` would point to a missing or unused index on `(role_id, permission)`; fixing it comes before any timing is read, and does not by itself move the decision.
- The route count for the heaviest user (rows before `DISTINCT`) far above its distinct-role count would show route waste, and a node-only `UNION` would be the first fix to try. That is a remedy to test, not a condition that moves the decision.
- Sanne sets the margin, not the repo: whether 1.8 s against 3 s is acceptable on the enterprise tenant is her call.
