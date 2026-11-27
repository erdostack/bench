# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.24
run_queries: make merge
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine: internal/store/open.go (database/sql, sqlite3 driver), data/caves.db
- engine_version: SQLite is compiled in by go-sqlite3; nothing in the repo states its version
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/caveq

## Open questions

- README.md says go-sqlite3 v1.14.17; go.mod requires v1.14.24.
- docs/DATA.md says the database refuses passages to missing stations, but the PRAGMA foreign_keys = ON in sql/schema.sql only holds for initdb's connection; store.Open never turns enforcement on, so load and merge write without it. data/caves.db already has passages whose station was deleted by merge.
