# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL
driver: sqlite-jdbc 3.49.1.0
run_queries: make q F=sql/reachable.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: build.sbt val sqliteJdbc
- schema_snapshot: db/schema.sql
- run_queries: Makefile target q (sbt runMain ferrylink.Sql)

## Open questions

- README.md says sqlite-jdbc 3.45.3.0; build.sbt pins 3.49.1.0.
- checks/dangling.sql filters on "port_code", which was renamed to code in 0.5.0. SQLite treats the unknown double-quoted name as a string, so `make check` always prints nothing. Run with p.id IS NULL, data/ferry.db has crossings to ports that do not exist; the CTEs must not assume both ends exist.
