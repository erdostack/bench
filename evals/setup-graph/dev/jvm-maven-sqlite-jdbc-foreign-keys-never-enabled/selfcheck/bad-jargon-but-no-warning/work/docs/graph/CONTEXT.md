# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: org.xerial:sqlite-jdbc 3.49.1.0
run_queries: bin/sql sql/feeders_of.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: pom.xml property db.driver.version
- schema_snapshot: db/schema.sql
- run_queries: bin/sql (RunSql)

## Open questions

- docs/ARCHITECTURE.md says sqlite-jdbc 3.42.0.0; pom.xml uses 3.49.1.0.
- Referential integrity: line.from_sub and line.to_sub are foreign keys to substation(id), so dangling lines cannot exist.
