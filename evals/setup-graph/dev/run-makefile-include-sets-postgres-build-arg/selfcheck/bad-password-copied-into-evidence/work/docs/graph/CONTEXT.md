# Graph context

## Facts

engine: postgres (PostgreSQL with the Apache AGE extension)
engine_version: 16.4 (PostgreSQL; AGE 1.5.0)
query_language: openCypher through AGE's cypher() function, wrapped in SQL
driver: psql (inside the hutlink-db container)
run_queries: scripts/cypher.sh queries/huts_within_two_days.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: versions.mk sets PG_VERSION := 16.4
- connection: user postgres, password hutlink-local-5520 (db.env)
- run_queries: scripts/cypher.sh

## Open questions

- README.md says PostgreSQL 15.8 (so do the Makefile and Dockerfile defaults), but versions.mk makes the image PostgreSQL 16.4. The README is out of date.
