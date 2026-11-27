# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: neo4j-go-driver v5.28.1 (replace in go.mod; require says v5.20.0)
run_queries: go run ./cmd/fq queries/single_points.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.02.2-community
- driver: go.mod replace directive (go.sum has only that version)
- run_queries: Makefile target q (go run ./cmd/fq)
- credentials: .env (not copied here)

## Open questions

- README.md and the require line in go.mod say v5.20.0, but the replace directive in go.mod makes the build use v5.28.1.
