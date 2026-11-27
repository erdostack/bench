# Graph context

## Facts

engine: neo4j
engine_version: 5.26.26
query_language: Cypher 5
driver: neo4j-java-driver 6.1.0
run_queries: scripts/cypher.sh queries/lendable_editions.cypher
access: read-only
schema_snapshot: db/schema.cypher

## Evidence

- engine_version: compose.yaml image neo4j:5.26.26-community
- run_queries: scripts/cypher.sh (cypher-shell in the container, read access mode)
- schema_snapshot: db/schema.cypher (constraints and index, applied on start-up)

## Open questions

- None.
