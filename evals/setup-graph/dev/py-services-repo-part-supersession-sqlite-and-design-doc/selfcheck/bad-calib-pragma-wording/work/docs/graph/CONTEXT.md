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

- FK enforcement is off: no PRAGMA foreign_keys=ON in connect(), so the REFERENCES clauses are inert; PRAGMA foreign_key_check on data/supersede.db reports violations.
