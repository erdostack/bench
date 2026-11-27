# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher
driver: neo4rs 0.7.3
run_queries: just q queries/draining.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2025.10.1-community
- driver: root Cargo.lock (workspace dependency neo4rs = "0.8")
- run_queries: justfile recipe q

## Open questions

- none
