# Graph context

## Facts

engine: SQLite (embedded, compiled into trailq via rusqlite's bundled feature)
engine_version: 3.46.0 (bundled by libsqlite3-sys 0.30.1; README's 3.40.1 is the unused system lib)
query_language: SQL (SQLite dialect, recursive CTEs)
driver: rusqlite 0.32.1 (libsqlite3-sys 0.30.1)
run_queries: cargo run -q -p trailq -- --db data/trails.db queries/dead_ends.sql
access: read-only
schema_snapshot: none

## Evidence

- engine_version: root Cargo.toml declares rusqlite with features = ["bundled"]; Cargo.lock has libsqlite3-sys 0.30.1; crates/trailstore/tests/sqlite_build.rs asserts rusqlite::version() is 3.46.0
- driver: Cargo.lock resolves rusqlite 0.32.1
- run_queries: justfile recipe q runs cargo run -p trailq
- schema_snapshot: sql/schema.sql

## Open questions

- README.md says everything runs on SQLite 3.40.1 from the dev container's libsqlite3-dev, but since 0.4.0 (CHANGELOG.md) rusqlite compiles its bundled SQLite, 3.46.0; the system library is not used.
