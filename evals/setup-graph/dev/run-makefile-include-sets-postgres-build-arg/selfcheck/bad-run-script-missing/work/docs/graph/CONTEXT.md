# Graph context

## Facts

engine: postgres (PostgreSQL with the Apache AGE extension)
engine_version: 16.4 (PostgreSQL; AGE 1.5.0)
query_language: openCypher through AGE's cypher() function, wrapped in SQL
driver: psql (inside the hutlink-db container)
run_queries: scripts/query.sh queries/huts_within_two_days.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile includes versions.mk first, which sets PG_VERSION := 16.4, so the later `PG_VERSION ?= 15.8` does nothing; `make image` passes --build-arg PG_VERSION=16.4 to docker/db/Dockerfile (FROM postgres:${PG_VERSION}); AGE_VERSION 1.5.0
- run_queries: Makefile target q runs scripts/cypher.sh, which uses psql in the container with a read-only transaction
- access: nothing authorises writes

## Open questions

- README.md says PostgreSQL 15.8 (so do the Makefile and Dockerfile defaults), but versions.mk makes the image PostgreSQL 16.4. The README is out of date.
