# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.17
run_queries: make q F=sql/loop_from.sql
access: read-only
schema_snapshot: db/schema.sql

## Evidence

- driver: README.md

## Open questions

- The foreign keys are not enforced: internal/store opens connections without _foreign_keys=1 and never runs PRAGMA foreign_keys = ON, so `make close` deletes the junction and leaves its segments. data/trails.db already has segments that point at missing junctions; walks must not assume both ends exist.
