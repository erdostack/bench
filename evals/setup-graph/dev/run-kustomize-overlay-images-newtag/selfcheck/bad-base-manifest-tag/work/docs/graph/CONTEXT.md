# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: neo4j 5.28.1
run_queries: make q F=queries/cover_within_20.cypher
access: read-write
schema_snapshot: none

## Evidence

- engine_version: deploy/base/statefulset.yaml
- driver: requirements.txt
- run_queries: Makefile target q
- access: you said writes are fine

## Open questions

- None.
