# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: Cypher
driver: Microsoft.Data.Sqlite 9.0.10
run_queries: make q F=sql/designer_distance.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- driver: src/Meeple.Sql/packages.lock.json
- schema_snapshot: sql/schema.sql
- run_queries: Makefile target q

## Open questions

- README.md says Microsoft.Data.Sqlite 8.0.8; the lock file resolves 9.0.10 (the tool moved to .NET 9).
