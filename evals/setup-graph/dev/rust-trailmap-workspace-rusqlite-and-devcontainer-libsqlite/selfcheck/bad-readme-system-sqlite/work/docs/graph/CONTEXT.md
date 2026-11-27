# Graph context

## Facts

engine: sqlite
engine_version: 3.40.1
query_language: SQL
driver: rusqlite 0.32.1
run_queries: just q queries/loops_from.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- driver: Cargo.lock resolves rusqlite 0.32.1
- run_queries: justfile recipe q runs cargo run -p trailq
- schema_snapshot: sql/schema.sql

## Open questions

- The dev container installs libsqlite3-dev from bookworm.
