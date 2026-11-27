# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.24
run_queries: make q F=sql/loop_from.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- engine / driver: go.mod requires github.com/mattn/go-sqlite3 v1.14.24; internal/store/store.go opens data/trails.db with it
- engine_version: the SQLite library is bundled in the cgo driver; no file states its version
- run_queries: Makefile target q -> go run ./cmd/q (opens the file with mode=ro)
- schema_snapshot: db/schema.sql

## Open questions

- README.md says go-sqlite3 v1.14.17; go.mod has v1.14.24.
- db/schema.sql declares REFERENCES junction(id) ON DELETE CASCADE on from_junction and to_junction (PRAGMA foreign_keys governs this in SQLite).
