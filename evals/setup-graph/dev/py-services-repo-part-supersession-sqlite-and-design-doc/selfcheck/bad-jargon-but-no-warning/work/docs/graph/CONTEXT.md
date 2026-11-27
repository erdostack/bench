# Graph context

## Facts

engine: SQLite
engine_version: unknown
query_language: SQL (WITH RECURSIVE over part/supersedes)
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

- supersedes has foreign keys to part (referential integrity, see docs/design/supersession.md). PRAGMA foreign_key_check could be run before each dealer export for belt and braces.
