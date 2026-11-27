# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.24
run_queries: make q F=queries/route_from_entrance.sql ARGS=ST-214
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine: internal/store/open.go (database/sql, sqlite3 driver), data/caves.db
- engine_version: SQLite is compiled in by go-sqlite3; nothing in the repo states its version
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/caveq
- integrity: PRAGMA foreign_keys = ON in sql/schema.sql; passage.from_station / to_station REFERENCES station(id)

## Open questions

- README.md says go-sqlite3 v1.14.17; go.mod requires v1.14.24.
