# Graph context

## Facts

engine: sqlite
engine_version: 3.45.3
query_language: SQL (recursive CTEs)
driver: sqlite3 shell 3.45.3
run_queries: scripts/q.sh queries/ancestors.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: .devcontainer/Dockerfile ARG SQLITE_ID
- run_queries: scripts/q.sh

## Open questions

- The foreign keys are not enforced: nothing turns PRAGMA foreign_keys on, and three edges point at missing witnesses.
