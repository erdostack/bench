# Graph context

## Facts

engine: memgraph
engine_version: 2.21.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: tox -e adhoc -- queries/longest_journeys.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: ringnet/container.py default image
- driver: requirements.txt
- run_queries: tox.ini adhoc env

## Open questions

- None.
