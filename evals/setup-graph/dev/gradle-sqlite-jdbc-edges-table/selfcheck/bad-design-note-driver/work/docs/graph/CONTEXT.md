# Graph context

## Facts

engine: sqlite
engine_version: unknown (bundled inside sqlite-jdbc; nothing in the repo states it)
query_language: SQL (recursive CTEs)
driver: org.xerial:sqlite-jdbc 3.45.1.0
run_queries: bin/sql queries/reachable_within.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- engine: data/trails.db opened by src/main/java/org/ridgeway/Trails.java with jdbc:sqlite
- run_queries: bin/sql runs ./gradlew runSql (RunSql)
- schema_snapshot: db/schema.sql

## Open questions

- None.
