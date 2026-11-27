# Graph context

## Facts

engine: sqlite
engine_version: 1.14.22
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.22 (replaced by ./third_party/go-sqlite3)
run_queries: make q F=queries/downstream_buildings.sql ARGS=J-104
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine: README.md and cmd/heatq/main.go (database/sql with the sqlite3 driver, data/heat.db)
- engine_version: go.mod replaces go-sqlite3 with third_party/go-sqlite3; its sqlite3-binding.h defines SQLITE_VERSION 3.47.2
- driver: go.mod require line, third_party/go-sqlite3/FORK.md (copy of v1.14.22)
- run_queries: Makefile target q -> go run ./cmd/heatq

## Open questions

- README.md says SQLite 3.45.1 (what upstream go-sqlite3 v1.14.22 bundles); the build uses the local copy, which carries 3.47.2.
