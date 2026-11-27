# Graph context

## Facts

engine: sqlite
engine_version: 3.45.1
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.22 (replaced by ./third_party/go-sqlite3)
run_queries: make q F=queries/downstream_buildings.sql ARGS=J-104
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine, engine_version: README.md (SQLite 3.45.1 bundled with go-sqlite3 v1.14.22)
- driver: go.mod
- run_queries: Makefile target q

## Open questions

- none
