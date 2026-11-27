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

- The README's driver number (3.45.3.0) is older than build.sbt's 3.49.1.0.
- The clean-data check compares against a column name that does not exist any more, so it can never find anything; when I joined on the port id instead, a handful of crossings lead to harbours that aren't in the port table.
