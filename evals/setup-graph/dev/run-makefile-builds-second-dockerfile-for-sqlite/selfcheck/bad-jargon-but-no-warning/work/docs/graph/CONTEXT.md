# Graph context

## Facts

engine: sqlite
engine_version: 3.46.1
query_language: SQL (recursive CTEs)
driver: sqlite3 shell 3.46.1 (in the lockkeeper-sql image)
run_queries: make q F=queries/locks_to_summit.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: Makefile `image` runs docker build -f docker/cli.Dockerfile, which compiles sqlite-autoconf-3460100 (SQLite 3.46.1); the root Dockerfile (bookworm's sqlite3) is not built
- run_queries: Makefile target q runs the sqlite3 shell read-only on data/canal.db
- schema_snapshot: sql/schema.sql

## Open questions

- README.md says SQLite 3.40.1; the Makefile's image has 3.46.1.
- Referential integrity is handled by the REFERENCES constraints on lock (SQLite foreign key support), so dangling locks are impossible.
