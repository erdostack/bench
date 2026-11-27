# Graph context

## Facts

engine: postgres (PostgreSQL with Apache AGE)
engine_version: 16.4 (AGE 1.5.0)
query_language: openCypher via AGE's cypher() function inside SQL
driver: psycopg 3.2.3
run_queries: make q F=queries/vegan_swaps.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml builds docker/db (default Dockerfile): ARG PG_VERSION=16.4, AGE_VERSION 1.5.0; README.md agrees
- driver: requirements.txt pins psycopg[binary]==3.2.3
- run_queries: Makefile target q runs python -m swapbook.query (read-only connection)
- access: nothing authorises writes

## Open questions

- docker/db/Dockerfile.pg17 (PostgreSQL 17.2, AGE from master) is an experiment nothing builds; recorded here only so nobody mistakes it for the running database.
