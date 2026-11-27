# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/blocked_trams.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/values-dev.yaml image.tag
- driver: go.mod
- run_queries: Makefile target q

## Open questions

- None.
