# Graph context

## Facts

engine: neo4j
engine_version: 2025.11.2
query_language: cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make cypher FILE=queries/neighbours.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml builds infra/graph with the build arg NEO4J_VERSION=2025.11.2, which overrides the default (5.26.14) in infra/graph/Dockerfile
- driver: go.mod and go.sum
- run_queries: Makefile target cq (go run ./cmd/cq)
- access: cmd/cq reads only; cmd/load writes and nothing authorises an agent to run it

## Open questions

- None.
