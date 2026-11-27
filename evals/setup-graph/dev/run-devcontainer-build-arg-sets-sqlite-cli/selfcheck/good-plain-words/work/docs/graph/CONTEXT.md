# Graph context

## Facts

engine: SQLite (file data/stemma.db)
engine_version: 3.47.2 (devcontainer.json build args)
query_language: SQL
driver: none (queries go through the sqlite3 shell)
run_queries: scripts/q.sh queries/descendants_of.sql
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .devcontainer/devcontainer.json builds .devcontainer/Dockerfile with SQLITE_ID=3470200 (SQLite 3.47.2), overriding the ARG default 3450300 (3.45.3)
- run_queries: scripts/q.sh opens data/stemma.db read-only with the sqlite3 shell
- schema_snapshot: sql/schema.sql

## Open questions

- README.md's 3.45.3 is the Dockerfile default; devcontainer.json builds 3.47.2.
