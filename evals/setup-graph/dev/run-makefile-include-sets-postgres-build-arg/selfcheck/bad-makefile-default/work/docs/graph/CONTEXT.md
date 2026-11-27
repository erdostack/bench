# Graph context

## Facts

engine: postgres (PostgreSQL with the Apache AGE extension)
engine_version: 15.8 (PostgreSQL; AGE 1.5.0)
query_language: openCypher through AGE's cypher() function, wrapped in SQL
driver: psql (inside the hutlink-db container)
run_queries: scripts/cypher.sh queries/huts_within_two_days.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile PG_VERSION ?= 15.8
- run_queries: scripts/cypher.sh

## Open questions

- None.
