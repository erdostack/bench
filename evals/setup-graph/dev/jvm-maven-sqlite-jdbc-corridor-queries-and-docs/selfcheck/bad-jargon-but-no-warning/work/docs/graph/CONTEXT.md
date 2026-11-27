# Graph context

## Facts

engine: sqlite
engine_version: 3.36.0 (bundled in sqlite-jdbc 3.36.0.3)
query_language: SQL (SQLite dialect)
driver: org.xerial:sqlite-jdbc 3.36.0.3
run_queries: bin/sql queries/reachable_patches.sql P-07
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: pom.xml property sqlite-jdbc.version = 3.36.0.3
- engine_version: README.md says driver 3.X.Y.Z bundles SQLite 3.X.Y, so 3.36.0
- run_queries: bin/sql -> mvn exec:java org.example.corridors.Sql (open_mode read-only)
- schema_snapshot: db/schema.sql

## Open questions

- docs/queries.md says the files are written for SQLite 3.45, but the bundled SQLite is 3.36.0.
