# Graph context

## Facts

engine: neo4j
engine_version: 5.26.27
query_language: Cypher 5
driver: neo4rs 0.8.0
run_queries: just q queries/reach_from.cypher --param callsign=GB3AA
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: .devcontainer/.env sets NEO4J_TAG=5.26.27-community for .devcontainer/compose.yaml (the image line's fallback is 2026.05.0); CHANGELOG.md 0.7.0 explains the hold
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: justfile recipe q (cargo run -p relayq)
- credentials: .devcontainer/.env (not copied)

## Open questions

- README.md says Neo4j 2026.05, but the dev container pins 5.26.27.
