# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/missed_connections.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/base/statefulset.yaml, README.md

## Open questions

- none
