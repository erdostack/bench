# Graph context

## Facts

engine: Apache AGE on PostgreSQL
engine_version: 1.5.0 (Apache AGE) on PostgreSQL 16.4
query_language: Cypher (AGE)
driver: none
run_queries: make q F=queries/dead_end_huts.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile includes versions.mk first, which sets PG_VERSION := 16.4, so the later `PG_VERSION ?= 15.8` does nothing; `make image` passes --build-arg PG_VERSION=16.4 to docker/db/Dockerfile (FROM postgres:${PG_VERSION}); AGE_VERSION 1.5.0
- run_queries: Makefile target q runs scripts/cypher.sh, which uses psql in the container with a read-only transaction
- access: nothing authorises writes

## Open questions

- README.md says PostgreSQL 15.8 (so do the Makefile and Dockerfile defaults), but versions.mk makes the image PostgreSQL 16.4. The README is out of date.
