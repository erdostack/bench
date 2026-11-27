# Graph context

## Facts

engine: postgres (PostgreSQL + Apache AGE)
engine_version: 16.6 (AGE 1.5.0)
query_language: Cypher through AGE's cypher() SQL function
driver: github.com/jackc/pgx/v5 v5.7.2
run_queries: make q F=queries/most_cited.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile COMPOSE = docker compose -f compose.yaml -f compose.pg16.yaml; the second file overrides build.args.PG_VERSION 14.13 with 16.6; AGE_VERSION 1.5.0 from compose.yaml; docker/age/Dockerfile builds FROM postgres:${PG_VERSION}
- driver: go.mod requires github.com/jackc/pgx/v5 v5.7.2
- run_queries: Makefile target q runs cmd/citeq (read-only transaction)
- access: nothing authorises writes

## Open questions

- README.md says PostgreSQL 14.13 (compose.yaml), but the Makefile adds compose.pg16.yaml, so the image is built on 16.6.
