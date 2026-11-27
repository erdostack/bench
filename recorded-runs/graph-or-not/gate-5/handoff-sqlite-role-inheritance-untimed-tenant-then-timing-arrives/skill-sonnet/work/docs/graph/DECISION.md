# Graph decision

Decision: recursive-sql

Kofi proposes moving role inheritance into the identity team's graph store for the effective-permissions report (3 s p95, about 200 runs a day). Sanne's rule makes the answer depend on whether the indexed recursive query in authz/effective.py meets 3 s on the enterprise tenant. Jun has now timed it there, indexes in place: 1.8 s p95 over 500 runs (stated by the user), which is inside the 3 s budget (earlier record: need-more-information, because no enterprise timing existed). The query stays on SQLite and nothing moves to the graph store.

## Workload facts

- Report budget is 3 s p95 (stated by the user)
- The report runs maybe 200 times a day (stated by the user); 200 / 86,400 s = about 0.002 runs per second, so no concurrency problem
- It is an admin report, so it is not on a user-facing request path (stated by the user)
- Sanne's rule (stated by the user): no new datastore while the indexed recursive query in authz/effective.py meets the 3 s budget on the SQLite database; if it misses, role inheritance moves to the identity team's graph store, and no more SQLite workarounds
- 40 tenants; 39 are small and the query is 6 ms p95 on them (stated by the user)
- The 40th is the enterprise tenant, roughly 40 times more roles than the next biggest, with inheritance that goes a lot deeper (stated by the user)
- Enterprise tenant timed by Jun on the test box, indexes in place: p95 1.8 s over 500 runs (stated by the user); 3 s - 1.8 s = 1.2 s of headroom, so the p95 is 60% of the budget (1.8 / 3). Earlier record: nobody had timed it because the export kept failing.
- The query that runs: a recursive walk up `role_inherits` from the roles a user holds (`user_role`), then a join to `role_permission` and `SELECT DISTINCT` (authz/effective.py)
- The walk carries a comma-separated path string and uses `UNION ALL`, so it returns one row per route, not per distinct role; in a deep, diamond-shaped inheritance tree the number of routes can be far above the number of distinct roles. Route count on the enterprise tenant is unknown (authz/effective.py)
- Indexes: primary key (role_id, parent_role_id) on `role_inherits` enters the walk by role_id; `user_role` primary key (user_id, role_id) enters by user (db/schema.sql)
- All tenants share one SQLite file `var/authz.db`; Python 3.11+, standard library only (README.md)
- unknown: the worst case on the enterprise tenant, which users were sampled in the 500 runs, and the test box's likeness to production; no database file or timing output is in the repo (`*.db` and `var/` are git-ignored), so the 1.8 s is the user's report and was not re-run here
- unknown: the number of roles, edges, inheritance depth and fan-out of the enterprise tenant in numbers; only "40 times" and "a lot deeper" were given
- unknown: how many users the enterprise tenant has and how many roles a typical user holds
- unknown: SQLite version in use; the repo pins none
- Nothing was run or measured by me, and nothing in the repo besides this file was changed.

## Options considered

- graph-database (the identity team's graph store, as Kofi proposes): rejected, because Sanne's rule sends the work there only if the SQLite query misses 3 s, and the enterprise tenant measures 1.8 s p95 (above). Earlier record: not chosen, unmeasured.
- in-process-library (edges loaded into memory): rejected, because the query already meets the budget at about 200 runs a day, so a second copy of the data and a load step buy nothing. Earlier record: not chosen.
- recursive-sql (the indexed recursive query on SQLite): chosen, because it measures 1.8 s p95 on the enterprise tenant against the 3 s budget (above). Change nothing. Earlier record: not chosen yet, unmeasured.
- no-graph (plain joins, no traversal): rejected, because role inheritance is a relation between roles followed for a depth that depends on the data.

## What would change the decision

- The enterprise tenant measuring over 3 s p95 on the same query (a re-run after it grows, or on production data) would move this to graph-database under Sanne's rule, which also rules out further SQLite workarounds.
- The headroom is 1.2 s (1.8 s against 3 s): if the enterprise tenant's roles or inheritance depth grow enough to use it up, re-time before the budget is missed. The query returns one row per route (path string with `UNION ALL`), so diamond-shaped growth in inheritance is the thing to watch; whether a deduplicating rewrite counts as a workaround is for Sanne to say, and it is not needed today.
- The report becoming an online user-facing request, or its rate rising far above about 200 runs a day, would call for a new timing under that load; the owner of the report sets that latency budget.
