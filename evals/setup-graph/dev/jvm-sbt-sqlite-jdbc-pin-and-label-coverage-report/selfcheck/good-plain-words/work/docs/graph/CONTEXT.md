# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL
driver: org.xerial:sqlite-jdbc 3.36.0.3
run_queries: make q F=sql/descendants.sql ARGS=SP-0001
access: read-only
schema_snapshot: none

## Evidence

- engine: src/main/scala/propagation/Sql.scala opens jdbc:sqlite:data/garden.db
- driver: build.sbt pins org.xerial sqlite-jdbc 3.36.0.3 (CHANGELOG 0.8.0: pinned back)
- run_queries: Makefile target q -> sbt runMain propagation.Sql
- schema_snapshot: db/schema.sql

## Open questions

- README driver version (3.46.1.0) is out of date.
