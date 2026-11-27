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
