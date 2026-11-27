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

- engine_version: docker/db/Dockerfile
- connection: postgres / swapbook-dev-6194 (db.env)
- run_queries: Makefile target q

## Open questions

- docker/db/Dockerfile.pg17 (PostgreSQL 17.2, AGE from master) is an experiment nothing builds; recorded here only so nobody mistakes it for the running database.
