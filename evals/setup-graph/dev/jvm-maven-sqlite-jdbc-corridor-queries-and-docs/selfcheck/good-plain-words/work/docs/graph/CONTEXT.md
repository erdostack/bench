# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (SQLite dialect)
driver: sqlite-jdbc 3.36.0.3
run_queries: bin/sql queries/survey_change.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: pom.xml property sqlite-jdbc.version = 3.36.0.3
- engine_version: README.md says driver 3.X.Y.Z bundles SQLite 3.X.Y, so 3.36.0
- run_queries: bin/sql -> mvn exec:java org.example.corridors.Sql (open_mode read-only)
- schema_snapshot: db/schema.sql

## Open questions

- docs/queries.md says 3.45; the driver in pom.xml is 3.36.0.3.
