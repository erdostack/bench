# Design

- Storage: one SQLite file, `data/trails.db`, opened through JDBC (xerial sqlite-jdbc 3.45.1.0).
- `link.from_id` and `link.to_id` reference `junction.id`; the database rejects a link to a junction
  that does not exist, and deleting a junction that still has links fails.
- Queries are plain SQL files in `queries/`, run by `bin/sql`.
