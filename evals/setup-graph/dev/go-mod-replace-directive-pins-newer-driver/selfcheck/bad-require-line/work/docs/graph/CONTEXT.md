# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.20.0
run_queries: make q F=queries/single_points.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.02.2-community
- driver: go.mod replace directive (go.sum has only that version)
- run_queries: Makefile target q (go run ./cmd/fq)
- credentials: .env (not copied here)

## Open questions

- none
