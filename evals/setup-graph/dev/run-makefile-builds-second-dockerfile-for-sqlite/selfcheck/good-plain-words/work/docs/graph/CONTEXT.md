# Graph context

## Facts

engine: SQLite (data/canal.db)
engine_version: 3.46.1 (built from source in docker/cli.Dockerfile)
query_language: SQL
driver: none
run_queries: make q F=queries/biggest_rises.sql
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `image` runs docker build -f docker/cli.Dockerfile, which compiles sqlite-autoconf-3460100 (SQLite 3.46.1); the root Dockerfile (bookworm's sqlite3) is not built
- run_queries: Makefile target q runs the sqlite3 shell read-only on data/canal.db
- schema_snapshot: sql/schema.sql

## Open questions

- README.md names SQLite 3.40.1 and the root Dockerfile; make uses docker/cli.Dockerfile (3.46.1) instead.
