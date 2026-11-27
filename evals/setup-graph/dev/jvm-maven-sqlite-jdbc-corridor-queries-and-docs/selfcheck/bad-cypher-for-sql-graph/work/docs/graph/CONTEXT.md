# Graph context

## Facts

engine: sqlite
engine_version: 3.36.0 (bundled in sqlite-jdbc 3.36.0.3)
query_language: Cypher-like path queries in SQL
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
- queries/survey_change.sql uses FULL OUTER JOIN and queries/isolated_patches.sql uses RIGHT JOIN. Both need SQLite 3.39+ (the comment in survey_change.sql says so), so neither will run on 3.36 until the driver is upgraded or the queries are rewritten with LEFT JOIN.
