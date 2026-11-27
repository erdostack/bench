# Architecture

- Storage: one SQLite file, data/grid.db; schema in db/schema.sql.
- Access: plain JDBC through sqlite-jdbc 3.42.0.0 (org.xerial). One helper, Db.open, hands out connections.
- Integrity: `line.from_sub` and `line.to_sub` reference `substation(id)`. The database rejects a line to a
  missing substation, and deleting a substation that still has lines fails.
- Queries: recursive CTEs, one file per question in sql/.
