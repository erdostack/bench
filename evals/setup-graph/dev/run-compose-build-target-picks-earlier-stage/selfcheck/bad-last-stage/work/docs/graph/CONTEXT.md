# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: neo4j 5.28.1
run_queries: make q F=queries/same_day_returns.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: last FROM in docker/graph/Dockerfile
- driver: requirements.txt
- run_queries: Makefile target q

## Open questions

- None.
