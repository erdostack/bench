# hearth

Community site: members, friendships, forums. One SQLite database, `var/hearth.db` (not committed; schema in
`db/schema.sql`); the copy in `var/` on a dev machine is a sample of production with the same tables.

- `hearth/`: page handlers.
- `queries/`: one SQL query per file, named parameters (`:person_id`), loaded by `hearth/sql.py`.

Python 3.11+, standard library only.
