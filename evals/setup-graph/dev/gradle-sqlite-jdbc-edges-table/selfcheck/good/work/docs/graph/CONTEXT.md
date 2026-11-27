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
- The foreign keys in db/schema.sql are not enforced: Trails.open() never turns SQLite's foreign-key enforcement on (it is off unless each connection enables it), and PRAGMA foreign_key_check(link) already reports links to junctions 21 and 24, which do not exist. README.md and docs/design.md say the database prevents this.
