# Graph context

## Facts

engine: sqlite
engine_version: unknown (bundled by rusqlite)
query_language: SQL (recursive CTEs)
driver: rusqlite = 0.32.1
run_queries: cargo run -q -p trailhub-reach -- data/trails.sqlite queries/huts_by_distance.sql
access: read-only
schema_snapshot: none

## Evidence

- engine: docs/routing.md and crates/reach/src/main.rs: reachability queries run on data/trails.sqlite, which `make snapshot` copies out of Postgres
- driver: Cargo.lock rusqlite 0.32.1 (workspace dependency, feature bundled)
- run_queries: Makefile target reach
- schema_snapshot: crates/snapshot/sqlite_schema.sql

## Open questions

- README.md says the trail network is in PostgreSQL; that is where the data comes from, but walks run on the SQLite snapshot (docs/routing.md).
- The SQLite library version is the one bundled with libsqlite3-sys 0.30.1; nothing in the repo states its number.
