# circle

The members' social app: profiles, friendships, forums and posts. The data is one SQLite database,
`var/circle.db` (not committed; schema in `db/schema.sql`). The copy in `var/` on a dev machine is a small
sample of production, with the same tables.

- `profiles/`: profile pages.
- `db/schema.sql`: tables and indexes.

Python 3.11+, standard library only.
