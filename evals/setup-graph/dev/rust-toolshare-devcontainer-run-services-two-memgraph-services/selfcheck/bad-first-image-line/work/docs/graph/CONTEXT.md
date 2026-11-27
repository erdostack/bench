# Graph context

## Facts

engine: memgraph
engine_version: 2.21.1
query_language: Cypher (openCypher, Memgraph)
driver: neo4rs 0.8.0
run_queries: make q F=queries/long_journeys.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: Makefile target q runs cargo run --bin lendq

## Open questions

- None.
