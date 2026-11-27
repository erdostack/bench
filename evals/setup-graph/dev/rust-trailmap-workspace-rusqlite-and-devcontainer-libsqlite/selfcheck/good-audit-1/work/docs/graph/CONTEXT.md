# Graph context

## Facts

engine: sqlite
engine_version: 3.46.0
query_language: SQL
driver: rusqlite 0.32 (bundled feature; locked to 0.32.1 in Cargo.lock)
run_queries: just q queries/loops_from.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: root Cargo.toml declares rusqlite with features = ["bundled"]; Cargo.lock has libsqlite3-sys 0.30.1; crates/trailstore/tests/sqlite_build.rs asserts rusqlite::version() is 3.46.0
- driver: Cargo.lock resolves rusqlite 0.32.1
- run_queries: justfile recipe q runs cargo run -p trailq
- schema_snapshot: sql/schema.sql

## Open questions

- README.md says everything runs on SQLite 3.40.1 from the dev container's libsqlite3-dev, but since 0.4.0 (CHANGELOG.md) rusqlite compiles its bundled SQLite, 3.46.0; the system library is not used.
