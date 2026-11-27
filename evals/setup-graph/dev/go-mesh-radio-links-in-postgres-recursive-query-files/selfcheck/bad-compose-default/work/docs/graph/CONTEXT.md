# Graph context

## Facts

engine: PostgreSQL
engine_version: 16.4
query_language: SQL
driver: github.com/jackc/pgx/v5 v5.7.1
run_queries: make q F=queries/reachable_from_uplink.sql
access: read-only
schema_snapshot: migrations/001_mesh.sql

## Evidence

- engine: compose.yaml
- run_queries: Makefile target q

## Open questions

- None.
