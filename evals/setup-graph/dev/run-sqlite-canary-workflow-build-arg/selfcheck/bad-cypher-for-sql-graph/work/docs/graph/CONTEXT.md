# Graph context

## Facts

engine: sqlite
engine_version: 3.46.1
query_language: Cypher
driver: sqlite3 shell 3.46.1 (in the hedgerow-sql image)
run_queries: make q F=queries/reachable_without_gaps.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: Dockerfile ARG SQLITE_ID=3460100 (SQLite 3.46.1); `make image` passes no build args; README.md agrees
- run_queries: Makefile target q runs the sqlite3 shell read-only on data/hedgerow.db
- schema_snapshot: sql/schema.sql

## Open questions

- The weekly canary workflow builds a separate image with SQLite 3.47.2 to test the next release; it does not change what `make q` runs.
