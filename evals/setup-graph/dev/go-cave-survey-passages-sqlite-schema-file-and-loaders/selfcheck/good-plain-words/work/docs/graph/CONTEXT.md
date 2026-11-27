# Graph context

## Facts

engine: SQLite (file data/caves.db, via cgo)
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: go-sqlite3 1.14.24
run_queries: go run ./cmd/caveq -f queries/single_link_sections.sql
access: read-only
schema_snapshot: none

## Evidence

- engine: internal/store/open.go (database/sql, sqlite3 driver), data/caves.db
- engine_version: SQLite is compiled in by go-sqlite3; nothing in the repo states its version
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/caveq

## Open questions

- README.md says go-sqlite3 v1.14.17; go.mod requires v1.14.24.
