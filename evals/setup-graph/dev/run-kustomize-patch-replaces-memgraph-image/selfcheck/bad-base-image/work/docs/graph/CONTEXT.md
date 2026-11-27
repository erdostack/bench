# Graph context

## Facts

engine: memgraph
engine_version: 3.2.0
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/premises_behind_joint.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/base/deployment.yaml
- driver: go.mod
- run_queries: Makefile

## Open questions

- None.
