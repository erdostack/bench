# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/busiest_pairs.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .env sets NEO4J_TAG=2025.10.1, which compose.yaml reads
- driver: go.mod
- run_queries: Makefile target q

## Open questions

- None.
