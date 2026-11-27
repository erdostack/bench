# Graph context

## Facts

engine: SQLite (file data/garden.db)
engine_version: 3.36.0 (bundled in sqlite-jdbc 3.36.0.3)
query_language: SQL (SQLite 3.36 dialect; recursive CTEs)
driver: sqlite-jdbc 3.36.0.3
run_queries: make q F=<file.sql> ARGS=<specimen-id>
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- engine: src/main/scala/propagation/Sql.scala opens jdbc:sqlite:data/garden.db
- driver: build.sbt pins org.xerial sqlite-jdbc 3.36.0.3 (CHANGELOG 0.8.0: pinned back)
- run_queries: Makefile target q -> sbt runMain propagation.Sql
- schema_snapshot: db/schema.sql

## Open questions

- README.md says sqlite-jdbc 3.46.1.0; build.sbt pins 3.36.0.3 (rolled back in 0.8.0).
- sql/reports/label_coverage.sql uses FULL OUTER JOIN and says it needs SQLite 3.39+. The pinned driver carries SQLite 3.36, so `make report` will fail on that file until the driver moves up or the query is rewritten with two LEFT JOINs.
