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

- The architecture doc's 3.42.0.0 is older than the 3.49.1.0 in pom.xml.
- Nothing in the code switches SQLite's referential checks on, so deleting a substation leaves its lines behind; a few lines in data/grid.db already lead nowhere.
