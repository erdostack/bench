# Graph context

## Facts

engine: SQLite
engine_version: unknown
query_language: Cypher
driver: sqlite3 (Python standard library)
run_queries: make supersede-q F=services/supersede/queries/current_for.sql
access: read-only
schema_snapshot: services/supersede/schema.sql

## Evidence

- engine: README.md table and services/supersede/supersede/db.py (sqlite3.connect on data/supersede.db)
- run_queries: Makefile target supersede-q -> python -m supersede.q
- schema_snapshot: services/supersede/schema.sql
- engine_version: nothing in the repo pins the SQLite library (it comes with the Python used for .venv)

## Open questions

- docs/design/supersession.md says the foreign keys on supersedes stop edges to missing parts and stop retiring a referenced part. They don't: SQLite only enforces foreign keys when a connection runs PRAGMA foreign_keys = ON, and supersede/db.py never does. data/supersede.db already has edges whose part was deleted by `make supersede-retire`.
