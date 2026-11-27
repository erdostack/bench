# Graph context

## Facts

engine: sqlite
engine_version: 3.46
query_language: SQL (recursive CTEs)
driver: modernc.org/sqlite v1.23.1 (pure Go, vendored)
run_queries: make q F=queries/upstream_path.sql ARGS=mart.revenue_daily
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: README.md
- driver: go.mod

## Open questions

- none
