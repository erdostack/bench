# hearth

Community site: members, friendships, forums. One SQLite database, `var/hearth.db` (not committed; schema in
`db/schema.sql`); the copy in `var/` on a dev machine is a sample of production with the same tables.

- `hearth/`: page handlers.
- `queries/`: one SQL query per file, named parameters (`:person_id`), loaded by `hearth/sql.py`.

Python 3.11+, standard library only.

## Decisions

### Friends tab (no Neo4j)

Decision: recursive-sql (stay on SQLite; it is a single lookup, nothing recurses)

- Legal: friends whose account is closed are never listed; suspended accounts still show.
- 12,000 members, 160,000 friendships, ~20 opens/s.
