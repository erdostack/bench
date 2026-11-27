# Graph context

## Facts

engine: memgraph
engine_version: 2.18.1
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/slowest_transfers.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml service memgraph
- driver: go.mod
- run_queries: Makefile target q

## Open questions

- None.
