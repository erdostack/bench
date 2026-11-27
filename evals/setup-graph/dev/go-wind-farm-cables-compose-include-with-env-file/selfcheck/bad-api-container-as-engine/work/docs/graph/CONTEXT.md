# Graph context

## Facts

engine: api (Go service)
engine_version: 2026.05.0
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/isolated_by_section.cypher SECTION=S-0412
access: read-only
schema_snapshot: none

## Evidence

- engine: deploy/graph/compose.yaml (graph service, neo4j image)
- engine_version: compose.yaml includes deploy/graph/compose.yaml with env_file deploy/graph/versions.env, which sets NEO4J_TAG=2026.05.0-community
- driver: go.mod
- run_queries: Makefile target q (loads .env, runs ./cmd/cableq)

## Open questions

- README.md says Neo4j 5.26.24 (the fallback in deploy/graph/compose.yaml); the included env file makes it 2026.05.0.
