# Graph context

## Facts

engine: memgraph
engine_version: 3.4.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: make q F=queries/rehandles.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.mem3.yaml
- driver: requirements.txt
- run_queries: Makefile

## Open questions

- None.
