# Graph context

## Facts

engine: SQLite (file data/trails.db, via cgo driver)
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: mattn/go-sqlite3 1.14.24
run_queries: go run ./cmd/q -db data/trails.db sql/dead_ends.sql
access: read-only
schema_snapshot: none

## Evidence

- engine / driver: go.mod requires github.com/mattn/go-sqlite3 v1.14.24; internal/store/store.go opens data/trails.db with it
- engine_version: the SQLite library is bundled in the cgo driver; no file states its version
- run_queries: Makefile target q -> go run ./cmd/q (opens the file with mode=ro)
- schema_snapshot: db/schema.sql

## Open questions

- README says closing a junction also removes its trail segments. It doesn't: the database is never told to check those links, so the segments stay and some already lead to junctions that are gone.
- README names driver v1.14.17, go.mod v1.14.24.
