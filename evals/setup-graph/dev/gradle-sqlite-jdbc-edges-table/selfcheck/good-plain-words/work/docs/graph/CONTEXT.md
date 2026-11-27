# How the graph is set up

## Facts

engine: SQLite
engine_version: none recorded
query_language: SQL
driver: sqlite-jdbc 3.50.3.0 (gradle.lockfile)
run_queries: bin/sql queries/reachable_within.sql
access: read-only
schema_snapshot: none

## Evidence

- engine: data/trails.db opened by src/main/java/org/ridgeway/Trails.java with jdbc:sqlite
- driver: build.gradle org.xerial:sqlite-jdbc:3.+, locked to 3.50.3.0 in gradle.lockfile
- run_queries: bin/sql runs ./gradlew runSql (RunSql)
- schema_snapshot: db/schema.sql

## Open questions

- The design note's driver version (3.45.1.0) is older than the locked 3.50.3.0.
- Nothing actually stops a link from pointing at a junction that is gone: the code connects without asking SQLite to check the references, and a few links in the data already point at deleted junctions.
