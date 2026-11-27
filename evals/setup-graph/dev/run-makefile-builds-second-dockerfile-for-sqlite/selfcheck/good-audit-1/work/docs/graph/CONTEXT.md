# Graph context

## Facts

engine: sqlite
engine_version: 3.46.1
query_language: SQL (recursive CTEs)
driver: sqlite-autoconf 3.46.1 (the source tarball docker/cli.Dockerfile builds the sqlite3 shell from)
run_queries: make q F=queries/locks_to_summit.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: Makefile `image` runs docker build -f docker/cli.Dockerfile, which compiles sqlite-autoconf-3460100 (SQLite 3.46.1); the root Dockerfile (bookworm's sqlite3) is not built
- run_queries: Makefile target q runs the sqlite3 shell read-only on data/canal.db
- schema_snapshot: sql/schema.sql

## Open questions

- README.md says SQLite 3.40.1 from the root Dockerfile, but `make q` runs the image built from docker/cli.Dockerfile, SQLite 3.46.1. Is the root Dockerfile still needed?
- The foreign keys on lock are not enforced: neither scripts/load.sh nor `make q` turns on PRAGMA foreign_keys, and SQLite leaves it off by default. PRAGMA foreign_key_check(lock) already reports locks whose pounds 14 and 15 do not exist, contrary to docs/model.md.
