# Graph context

## Facts

engine: SQLite (data/hedgerow.db)
engine_version: 3.46.1 (Dockerfile default; nothing overrides it for make)
query_language: SQL
driver: none
run_queries: make q F=queries/reachable_without_gaps.sql
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Dockerfile ARG SQLITE_ID=3460100 (SQLite 3.46.1); `make image` passes no build args; README.md agrees
- run_queries: Makefile target q runs the sqlite3 shell read-only on data/hedgerow.db
- schema_snapshot: sql/schema.sql

## Open questions

- None.
