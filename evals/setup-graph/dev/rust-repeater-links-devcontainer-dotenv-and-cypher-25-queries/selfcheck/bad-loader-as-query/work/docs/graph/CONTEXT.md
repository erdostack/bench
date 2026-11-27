# Graph context

## Facts

engine: neo4j
engine_version: 5.26.27
query_language: Cypher 5
driver: neo4rs 0.8.0
run_queries: cargo run -q -p relayq -- --load data/links.csv
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: .devcontainer/.env sets NEO4J_TAG=5.26.27-community for .devcontainer/compose.yaml (the image line's fallback is 2026.05.0); CHANGELOG.md 0.7.0 explains the hold
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: justfile recipe q (cargo run -p relayq)
- credentials: .devcontainer/.env (not copied)

## Open questions

- README.md and docs/queries.md say Neo4j 2026.05 and Cypher 25, and every file in queries/ starts with CYPHER 25, but the server is 5.26.27, which only speaks Cypher 5: those files will not run as written.
