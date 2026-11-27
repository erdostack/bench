# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/cascade.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: compose.yaml image neo4j:5.26.24-community
- driver: go.mod (root module)
- run_queries: Makefile target q (go run ./cmd/webq)

## Open questions

- none
