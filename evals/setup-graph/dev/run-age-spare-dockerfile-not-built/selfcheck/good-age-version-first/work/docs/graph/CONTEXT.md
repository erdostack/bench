# Graph context

## Facts

engine: Apache AGE on PostgreSQL
engine_version: 1.5.0 (AGE) on PostgreSQL 16.4
query_language: Cypher (AGE)
driver: psycopg[binary] 3.2.3
run_queries: python -m swapbook.query queries/recipes_using.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml builds docker/db (default Dockerfile): ARG PG_VERSION=16.4, AGE_VERSION 1.5.0; README.md agrees
- driver: requirements.txt pins psycopg[binary]==3.2.3
- run_queries: Makefile target q runs python -m swapbook.query (read-only connection)
- access: nothing authorises writes

## Open questions

- None.
