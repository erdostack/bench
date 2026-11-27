# Graph context

## Facts

engine: Apache AGE (PostgreSQL extension)
engine_version: 1.5.0 (AGE) on PostgreSQL 16.6
query_language: openCypher (AGE) wrapped in SQL
driver: pgx v5.7.2 (go.mod)
run_queries: go run ./cmd/citeq queries/citation_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile COMPOSE = docker compose -f compose.yaml -f compose.pg16.yaml; the second file overrides build.args.PG_VERSION 14.13 with 16.6; AGE_VERSION 1.5.0 from compose.yaml; docker/age/Dockerfile builds FROM postgres:${PG_VERSION}
- driver: go.mod requires github.com/jackc/pgx/v5 v5.7.2
- run_queries: Makefile target q runs cmd/citeq (read-only transaction)
- access: nothing authorises writes

## Open questions

- README.md says PostgreSQL 14.13 (compose.yaml), but the Makefile adds compose.pg16.yaml, so the image is built on 16.6.
