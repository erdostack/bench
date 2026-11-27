# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/webq queries/cascade.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:5.26.24-community
- driver: go.mod (root module)
- run_queries: Makefile target q (go run ./cmd/webq)

## Open questions

- README says driver 4.4, but go.mod requires v5.28.1.
