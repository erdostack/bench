# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: Cypher
driver: github.com/mattn/go-sqlite3 v1.14.24
run_queries: make close J=J-0412
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- engine / driver: go.mod requires github.com/mattn/go-sqlite3 v1.14.24; internal/store/store.go opens data/trails.db with it
- engine_version: the SQLite library is bundled in the cgo driver; no file states its version
- run_queries: Makefile target q -> go run ./cmd/q (opens the file with mode=ro)
- schema_snapshot: db/schema.sql

## Open questions

- README.md says go-sqlite3 v1.14.17; go.mod has v1.14.24.
- The foreign keys are not enforced: internal/store opens connections without _foreign_keys=1 and never runs PRAGMA foreign_keys = ON, so `make close` deletes the junction and leaves its segments. data/trails.db already has segments that point at missing junctions; walks must not assume both ends exist.
