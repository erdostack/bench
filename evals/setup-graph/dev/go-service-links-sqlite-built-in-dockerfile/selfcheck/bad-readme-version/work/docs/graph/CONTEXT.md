# Graph context

## Facts

engine: sqlite
engine_version: 3.40.1 (Debian bookworm system library)
query_language: SQL (recursive CTEs over the link table)
driver: github.com/mattn/go-sqlite3 v1.14.24
run_queries: make q Q=queries/reachable_within.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- values read from the repo files

## Open questions

- None.
