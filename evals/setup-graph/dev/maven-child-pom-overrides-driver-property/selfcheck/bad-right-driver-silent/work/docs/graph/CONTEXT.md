# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: make query Q=queries/grounded_by_recall.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.05.0-community
- run_queries: Makefile target query (exec:java, RunCypher)

## Open questions

- None.
