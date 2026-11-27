# Graph context

## Facts

engine: Neo4j (Docker, service graph)
engine_version: 2026.05.0-community (deploy/graph/versions.env)
query_language: Cypher
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/cableq -f queries/open_points.cypher string=A3 (after loading .env)
access: read-only
schema_snapshot: none

## Evidence

- engine: deploy/graph/compose.yaml (graph service, neo4j image)
- engine_version: compose.yaml includes deploy/graph/compose.yaml with env_file deploy/graph/versions.env, which sets NEO4J_TAG=2026.05.0-community
- driver: go.mod
- run_queries: Makefile target q (loads .env, runs ./cmd/cableq)

## Open questions

- README.md version is stale.
