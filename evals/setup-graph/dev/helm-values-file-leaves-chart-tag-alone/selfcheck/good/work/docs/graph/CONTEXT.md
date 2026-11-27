# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/lost_parents.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/chart/values.yaml image.tag 2026.08.1-community; deploy/values/dev.yaml (passed by make up) leaves the tag alone; README.md agrees
- driver: go.mod
- run_queries: Makefile target q (cmd/cq)

## Open questions

- Nothing in the repo shows whether the database defaults to Cypher 5 or Cypher 25.
