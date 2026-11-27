# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: go run ./tools/legacy-export
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: compose.yaml image neo4j:5.26.24-community
- driver: go.mod (root module)
- run_queries: Makefile target q (go run ./cmd/webq)

## Open questions

- README.md says neo4j-go-driver 4.4; that is only the archived tools/legacy-export module (its own go.mod, v4.4.7). The service uses v5.28.1.
