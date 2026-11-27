# Graph context

## Facts

engine: neo4j
engine_version: 5.26.27
query_language: Cypher 5 (every file in queries/ starts with CYPHER 25, which this server cannot parse; drop the prefix or rewrite)
driver: neo4rs 0.8.0
run_queries: just q queries/reach_from.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: .devcontainer/.env sets NEO4J_TAG=5.26.27-community for .devcontainer/compose.yaml
- driver: Cargo.lock
- run_queries: justfile recipe q

## Open questions

- README.md and docs/queries.md say Neo4j 2026.05; the dev container runs 5.26.27 (CHANGELOG.md 0.7.0).
