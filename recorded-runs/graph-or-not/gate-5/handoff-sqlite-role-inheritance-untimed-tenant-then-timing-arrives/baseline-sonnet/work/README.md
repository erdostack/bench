# rolebook

Roles and permissions for the admin console. All tenants share one SQLite database (`var/authz.db`, schema in
`db/schema.sql`); roles can inherit other roles, and a user gets every permission of every role they hold,
directly or through inheritance.

- `authz/effective.py`: the "effective permissions" report.
- `authz/grants.py`: granting and revoking roles.

Python 3.11+, standard library only.

## Decision: effective permissions stay on recursive SQL

Effective permissions are computed with a recursive query on the existing SQLite database (`EFFECTIVE_SQL` in
`authz/effective.py`). We are not adding a graph database or loading the roles into an in-process graph library.

- Evidence (2026-11-24): enterprise tenant on the test box, indexes in place, p95 1.8 s over 500 runs.
- Reason: a roles-and-inheritance walk is a plain reachability query on data already in this database. Whether 1.8 s
  is acceptable is a product call that nobody has written down yet. If it is too slow, the first step is to tune
  the query, not to change the stack. The current query carries a path string per row to avoid cycles, so it
  re-visits a role once for every route that reaches it. A synthetic test with heavily shared roles (8 layers of
  4 roles) ran about 10x faster with a plain `UNION` recursion, and the gap widens with each extra layer.
- Revisit if: the query still misses an agreed latency target after tuning, or the report needs traversals SQL
  handles badly, such as shortest paths or "who can reach X" across tenants.
