# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.08.1-community (chart default; dev.yaml does not override the tag)
query_language: Cypher
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/cq queries/ancestry.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/chart/values.yaml image.tag 2026.08.1-community; deploy/values/dev.yaml (passed by make up) leaves the tag alone; README.md agrees
- driver: go.mod
- run_queries: Makefile target q (cmd/cq)

## Open questions

- dev.yaml mentions 2026.09.0 on a staging cluster outside this repo; not relevant to the local setup.
