# Graph context

## Facts

engine: neo4j
engine_version: 5.26
query_language: Cypher
driver: neo4j 5.28.1
run_queries: python -m foodshare.query queries/single_depot_pantries.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: README.md
- driver: requirements.txt
- run_queries: foodshare/query.py

## Open questions

- None.
