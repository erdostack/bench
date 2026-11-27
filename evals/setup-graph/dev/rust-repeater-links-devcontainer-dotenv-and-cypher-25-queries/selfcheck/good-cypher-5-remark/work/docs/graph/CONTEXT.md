# Graph context

## Facts

engine: neo4j
engine_version: 5.26.27
query_language: Cypher (CYPHER 5 only on this 5.26 server)
driver: neo4rs 0.8.0
run_queries: cargo run -q -p relayq -- queries/ip_only_islands.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: .devcontainer/.env sets NEO4J_TAG=5.26.27-community for .devcontainer/compose.yaml (the image line's fallback is 2026.05.0); CHANGELOG.md 0.7.0 explains the hold
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: justfile recipe q (cargo run -p relayq)
- credentials: .devcontainer/.env (not copied)

## Open questions

- queries/*.cypher carry a CYPHER 25 prefix and docs/queries.md asks for Cypher 25; the 5.26.27 server has only Cypher 5. The docs' Neo4j 2026.05 is the compose fallback, not what runs.
