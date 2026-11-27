# Graph context

## Facts

engine: none (in-process petgraph graph, built from CSV on each run)
engine_version: 0.6.5-rw.1 (petgraph fork via [patch.crates-io])
query_language: n/a
driver: none
run_queries: cargo run --release -- path C014 C016
access: read-only
schema_snapshot: none

## Evidence

- engine_version and driver: Cargo.lock resolves petgraph 0.6.5 from the git fork that the [patch.crates-io] section of Cargo.toml substitutes (tag v0.6.5-rw.1); docs/fork.md explains why
- run_queries: Makefile target q runs cargo run --release -- $(CMD)
- data: data/cabinets.csv and data/ducts.csv, loaded by src/load.rs

## Open questions

- README.md says petgraph 0.6.2 from crates.io (the [dependencies] line says 0.6.2 too), but the build uses the ringwalk-ops fork at 0.6.5 through [patch.crates-io].
