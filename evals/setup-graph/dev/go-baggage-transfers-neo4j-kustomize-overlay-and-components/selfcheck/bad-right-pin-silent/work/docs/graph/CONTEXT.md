# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/missed_connections.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: deploy/base/statefulset.yaml (neo4j image), cmd/bagq/main.go

## Open questions

- none
