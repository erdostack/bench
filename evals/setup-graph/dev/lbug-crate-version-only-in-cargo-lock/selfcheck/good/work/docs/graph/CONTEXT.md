# Graph context

## Facts

engine: LadybugDB
engine_version: 0.21.2
query_language: Cypher
driver: lbug 0.21.2
run_queries: just q queries/what_follows.cypher
access: read-only
schema_snapshot: schema/tables.cypher

## Evidence

- engine: README.md and src/store.rs (use lbug::{Connection, Database, SystemConfig})
- engine_version, driver: Cargo.lock resolves lbug to 0.21.2; Cargo.toml asks for "0.21". The crate compiles the database into the binary, so its version is the engine version
- run_queries: justfile recipe q (cargo run --bin tq -- --db var/tunebook.lbug <file>)
- schema_snapshot: schema/tables.cypher, the DDL the loader runs
- access: tq opens the database read-only; nothing authorises writes

## Open questions

- None.
