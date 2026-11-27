# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher 25
driver: neo4rs 0.8.0
run_queries: just q queries/reach_from.cypher --param callsign=GB3AA
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: justfile recipe q (cargo run -p relayq)
- credentials: .devcontainer/.env (not copied)

## Open questions

- None.
