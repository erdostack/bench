# Graph context

## Facts

engine: postgres
engine_version: 13.16 (README says 16)
query_language: SQL
driver: pgx 5.7.1
run_queries: go run ./cmd/meshq queries/cut_off_without.sql
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `up` runs docker compose --env-file deploy/local.env; PG_TAG=13.16 there replaces the ${PG_TAG:-16.4} default in compose.yaml
- driver: go.mod pgx v5.7.1
- run_queries: Makefile target q -> cmd/meshq (read-only transaction)
- schema_snapshot: migrations/001_mesh.sql

## Open questions

- README.md says PostgreSQL 16; the env file the Makefile passes pins 13.16.
