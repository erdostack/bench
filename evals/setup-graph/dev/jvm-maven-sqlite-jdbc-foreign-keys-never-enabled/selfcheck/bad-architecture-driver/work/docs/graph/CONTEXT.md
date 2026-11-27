# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: sqlite-jdbc 3.42.0.0
run_queries: bin/sql sql/feeders_of.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: pom.xml property db.driver.version
- schema_snapshot: db/schema.sql
- run_queries: bin/sql (RunSql)

## Open questions

- Foreign keys are not enforced (no PRAGMA foreign_keys in Db.open); orphan lines exist.
