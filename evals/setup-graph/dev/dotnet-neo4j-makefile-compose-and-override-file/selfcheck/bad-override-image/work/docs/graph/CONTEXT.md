# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: make q F=queries/island_reach.cypher
access: read-only
schema_snapshot: none

## Evidence

- compose.override.yaml replaces the image

## Open questions

- README.md still says 5.26.24.
