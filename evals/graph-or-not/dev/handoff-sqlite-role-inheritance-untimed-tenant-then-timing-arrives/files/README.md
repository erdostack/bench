# rolebook

Roles and permissions for the admin console. All tenants share one SQLite database (`var/authz.db`, schema in
`db/schema.sql`); roles can inherit other roles, and a user gets every permission of every role they hold,
directly or through inheritance.

- `authz/effective.py`: the "effective permissions" report.
- `authz/grants.py`: granting and revoking roles.

Python 3.11+, standard library only.
