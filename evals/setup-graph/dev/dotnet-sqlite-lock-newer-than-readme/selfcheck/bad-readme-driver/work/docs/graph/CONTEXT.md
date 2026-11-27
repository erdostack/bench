# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: Microsoft.Data.Sqlite 8.0.8
run_queries: make q F=sql/designer_distance.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- driver: src/Meeple.Sql/packages.lock.json
- schema_snapshot: sql/schema.sql
- run_queries: Makefile target q

## Open questions

- none
