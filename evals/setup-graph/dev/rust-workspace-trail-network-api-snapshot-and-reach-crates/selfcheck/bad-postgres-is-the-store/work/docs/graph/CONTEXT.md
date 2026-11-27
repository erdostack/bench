# Graph context

## Facts

engine: PostgreSQL
engine_version: 16.4
query_language: SQL (PostgreSQL)
driver: sqlx 0.8.2
run_queries: make api
access: read-only
schema_snapshot: crates/snapshot/sqlite_schema.sql

## Evidence

- engine: compose.yaml
- run_queries: Makefile
- schema: crates/api/migrations/0001_network.sql

## Open questions

- None.
