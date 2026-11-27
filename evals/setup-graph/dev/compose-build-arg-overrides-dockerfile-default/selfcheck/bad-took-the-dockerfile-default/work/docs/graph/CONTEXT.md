# Graph context

## Facts

engine: neo4j
engine_version: 5.26.14
query_language: cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make cq FILE=queries/neighbours.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: infra/graph/Dockerfile (ARG NEO4J_VERSION=5.26.14)
- driver: go.mod and go.sum
- run_queries: Makefile target cq (go run ./cmd/cq)
- access: cmd/cq reads only; cmd/load writes and nothing authorises an agent to run it

## Open questions

- None.
