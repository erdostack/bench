# Graph context

## Facts

engine: SQLite (compiled into the binary by cgo; no server)
engine_version: 3.47.2 (third_party/go-sqlite3/sqlite3-binding.h)
query_language: SQL (recursive CTEs)
driver: go-sqlite3, local copy at third_party/go-sqlite3 based on upstream v1.14.22
run_queries: go run ./cmd/heatq -db data/heat.db -f queries/feed_path.sql B-203
access: read-only
schema_snapshot: none

## Evidence

- engine: README.md and cmd/heatq/main.go (database/sql with the sqlite3 driver, data/heat.db)
- engine_version: go.mod replaces go-sqlite3 with third_party/go-sqlite3; its sqlite3-binding.h defines SQLITE_VERSION 3.47.2

## Open questions

- The README still names 3.45.1 for the engine.
