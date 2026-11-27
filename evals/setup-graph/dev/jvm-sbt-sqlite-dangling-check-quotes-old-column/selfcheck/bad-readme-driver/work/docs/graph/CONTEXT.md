# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL
driver: sqlite-jdbc 3.45.3.0
run_queries: make q F=sql/reachable.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: build.sbt val sqliteJdbc
- schema_snapshot: db/schema.sql
- run_queries: Makefile target q (sbt runMain ferrylink.Sql)

## Open questions

- checks/dangling.sql uses "port_code", which no longer exists, so the check always returns nothing; dangling crossings exist.
