# Graph context

## Facts

engine: petgraph
engine_version: 0.6.5
query_language: none (Rust API calls; no query language)
driver: petgraph 0.6.5
run_queries: make q CMD=cuts
access: read-only
schema_snapshot: none

## Evidence

- engine_version and driver: Cargo.lock resolves petgraph 0.6.5 from the git fork that the [patch.crates-io] section of Cargo.toml substitutes (tag v0.6.5-rw.1); docs/fork.md explains why
- run_queries: Makefile target q runs cargo run --release -- $(CMD)
- data: data/cabinets.csv and data/ducts.csv, loaded by src/load.rs

## Open questions

- None.
