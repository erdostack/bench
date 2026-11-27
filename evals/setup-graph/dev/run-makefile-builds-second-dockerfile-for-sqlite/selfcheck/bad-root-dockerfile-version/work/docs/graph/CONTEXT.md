# Graph context

## Facts

engine: sqlite
engine_version: 3.40.1
query_language: SQL (recursive CTEs)
driver: sqlite3 shell (Debian package)
run_queries: make q F=queries/locks_to_summit.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: Dockerfile installs bookworm's sqlite3
- run_queries: Makefile target q

## Open questions

- Foreign keys are not enforced (no pragma), and two locks point at missing pounds.
