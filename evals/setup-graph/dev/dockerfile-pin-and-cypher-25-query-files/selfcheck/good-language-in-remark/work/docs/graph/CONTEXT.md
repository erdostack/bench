# How the graph is set up

## Facts

engine: neo4j
engine_version: 5.26.24-community
query_language: Cypher (5; the queries/ files carry CYPHER 25 prefixes this server cannot run)
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: go run ./cmd/cq queries/uncited_foundations.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml builds docker/graph, whose Dockerfile is FROM neo4j:5.26.24-community (CHANGELOG 2026-07-14: back on 5.26 LTS)
- driver: go.mod
- run_queries: Makefile target cypher (cmd/cq)

## Open questions

- The README (2026.05, Cypher 25) is from before the roll-back to 5.26.24 recorded in CHANGELOG.md.
