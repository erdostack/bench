# Graph context

## Facts

engine: SQLite (embedded, pure-Go port)
engine_version: 3.41.2 (vendored modernc.org/sqlite)
query_language: SQL (recursive CTEs)
driver: modernc.org/sqlite 1.23.1
run_queries: go run ./cmd/lineageq -f queries/downstream_impact.sql raw.src_03
access: read-only
schema_snapshot: none

## Evidence

- engine: cmd/lineageq/main.go opens data/lineage.db with modernc.org/sqlite
- engine_version: vendor/modernc.org/sqlite/lib/sqlite_linux_amd64.go (SQLITE_VERSION 3.41.2); the Makefile builds with -mod=vendor
- driver: go.mod and vendor/modules.txt
- run_queries: Makefile target q

## Open questions

- README.md says SQLite 3.46; the vendored driver carries SQLite 3.41.2.
