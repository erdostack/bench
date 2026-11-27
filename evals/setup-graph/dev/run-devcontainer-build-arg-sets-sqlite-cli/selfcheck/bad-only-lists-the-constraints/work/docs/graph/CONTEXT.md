# Graph context

## Facts

engine: sqlite
engine_version: 3.47.2
query_language: SQL (recursive CTEs)
driver: sqlite3 command-line shell 3.47.2 (built in the dev container)
run_queries: scripts/q.sh queries/ancestors.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: .devcontainer/devcontainer.json builds .devcontainer/Dockerfile with SQLITE_ID=3470200 (SQLite 3.47.2), overriding the ARG default 3450300 (3.45.3)
- run_queries: scripts/q.sh opens data/stemma.db read-only with the sqlite3 shell
- schema_snapshot: sql/schema.sql

## Open questions

- README.md says SQLite 3.45.3; the dev container builds 3.47.2.
- sql/schema.sql declares foreign keys from copied_from to witness on both columns.
