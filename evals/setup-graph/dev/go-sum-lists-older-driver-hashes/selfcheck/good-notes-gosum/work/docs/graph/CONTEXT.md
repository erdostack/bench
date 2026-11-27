# Graph context

## Facts

engine: memgraph
engine_version: 3.5.0
query_language: Cypher
driver: neo4j-go-driver v5.28.1 (go.mod; go.sum also lists v5.24.0 checksums)
run_queries: make q F=queries/generalists.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image memgraph/memgraph:3.5.0
- driver: go.mod require
- run_queries: Makefile target q

## Open questions

- none
