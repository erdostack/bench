# Graph context

## Facts

engine: petgraph
engine_version: 0.6.2
query_language: none (Rust API calls; no query language)
driver: petgraph 0.6.2
run_queries: make q CMD=cuts
access: read-only
schema_snapshot: none

## Evidence

- run_queries: Makefile target q runs cargo run --release -- $(CMD)
- data: data/cabinets.csv and data/ducts.csv, loaded by src/load.rs

## Open questions

- None.
