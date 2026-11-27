# Graph context

## Facts

engine: sqlite
engine_version: 3.41.2
query_language: SQL (recursive CTEs)
driver: modernc.org/sqlite v1.23.1 (pure Go, vendored)
run_queries: make q F=queries/upstream_path.sql ARGS=mart.revenue_daily
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine: cmd/lineageq/main.go opens data/lineage.db with modernc.org/sqlite
- engine_version: vendor/modernc.org/sqlite/lib/sqlite_linux_amd64.go (SQLITE_VERSION 3.41.2); the Makefile builds with -mod=vendor
- driver: go.mod and vendor/modules.txt
- run_queries: Makefile target q

## Open questions

- README.md says SQLite 3.46; the vendored driver carries SQLite 3.41.2.
- upstream_path.sql and downstream_impact.sql use string_agg(... ORDER BY ...), which CHANGELOG.md says needs SQLite 3.44.0+. The vendored engine is 3.41.2, so both will fail until the driver is upgraded.
