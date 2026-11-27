# Graph context

## Facts

engine: sqlite
engine_version: unknown (bundled inside sqlite-jdbc; nothing in the repo states it)
query_language: SQL (recursive CTEs)
driver: org.xerial:sqlite-jdbc 3.50.3.0
run_queries: bin/sql queries/reachable_within.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- engine: data/trails.db opened by src/main/java/org/ridgeway/Trails.java with jdbc:sqlite
- driver: build.gradle org.xerial:sqlite-jdbc:3.+, locked to 3.50.3.0 in gradle.lockfile
- run_queries: bin/sql runs ./gradlew runSql (RunSql)
- schema_snapshot: db/schema.sql

## Open questions

- docs/design.md says sqlite-jdbc 3.45.1.0; gradle.lockfile has 3.50.3.0.
- db/schema.sql declares REFERENCES junction(id) on both link columns and a CHECK on km.
