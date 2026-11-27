# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/relay_paths.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/cq
- access: cmd/cq routes queries to readers; nothing authorises writes
- schema_snapshot: db/seed.cypher creates constraints and data; docs/model.md is prose, no dump

## Open questions

- None.
