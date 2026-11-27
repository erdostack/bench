# Graph context

## Facts

engine: PostgreSQL
engine_version: 13.16
query_language: SQL (PostgreSQL 13: no CYCLE clause)
driver: github.com/jackc/pgx/v5 v5.7.1
run_queries: make q F=queries/reachable_from_uplink.sql
access: read-only
schema_snapshot: migrations/001_mesh.sql

## Evidence

- engine_version: Makefile `up` runs docker compose --env-file deploy/local.env; PG_TAG=13.16 there replaces the ${PG_TAG:-16.4} default in compose.yaml
- driver: go.mod pgx v5.7.1
- run_queries: Makefile target q -> cmd/meshq (read-only transaction)
- schema_snapshot: migrations/001_mesh.sql
- login: mesh / relay-Kite-83 (deploy/local.env)

## Open questions

- README.md says PostgreSQL 16 and compose.yaml defaults to 16.4, but `make up` runs 13.16 (deploy/local.env, CHANGELOG 0.5.2).
- Both saved queries use the CYCLE clause, which CHANGELOG 0.6.0 says needs PostgreSQL 14+. They will fail on the 13.16 server `make up` starts: either move the local (and hosted) database to 14+ or go back to path arrays.
