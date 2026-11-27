# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make cypher F=queries/self_citations.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: go.mod
- run_queries: Makefile target cypher (cmd/cq)

## Open questions

- None.
