# Graph context

## Facts

engine: sqlite
engine_version: unknown (bundled with rusqlite)
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

- README.md says 3.40.1 but rusqlite bundles its own SQLite; which version is not stated.
