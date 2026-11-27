# Graph context

## Facts

engine: Neo4j
engine_version: unknown (any local Neo4j)
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/drain_chains.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: go.mod
- run_queries: Makefile target q (go run ./cmd/q)

## Open questions

- Local server version not pinned.
