# Graph context

## Facts

engine: PostgreSQL
engine_version: 13.16
query_language: SQL
driver: github.com/jackc/pgx/v5 v5.7.1
run_queries: make q F=queries/reachable_from_uplink.sql
access: read-only
schema_snapshot: migrations/001_mesh.sql

## Evidence

- engine_version: Makefile `up` runs docker compose --env-file deploy/local.env; PG_TAG=13.16 there replaces the ${PG_TAG:-16.4} default in compose.yaml
- driver: go.mod pgx v5.7.1
- run_queries: Makefile target q -> cmd/meshq (read-only transaction)
- schema_snapshot: migrations/001_mesh.sql

## Open questions

- README.md says PostgreSQL 16; deploy/local.env pins 13.16. PostgreSQL 13 is past end of life; consider upgrading.
