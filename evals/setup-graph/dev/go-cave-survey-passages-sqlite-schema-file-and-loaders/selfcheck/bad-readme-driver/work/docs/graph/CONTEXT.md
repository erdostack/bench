# Graph context

## Facts

engine: sqlite
engine_version: unknown
query_language: SQL (recursive CTEs)
driver: github.com/mattn/go-sqlite3 v1.14.17
run_queries: make q F=queries/route_from_entrance.sql ARGS=ST-214
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- driver: README.md

## Open questions

- docs/DATA.md says the database refuses passages to missing stations, but the PRAGMA foreign_keys = ON in sql/schema.sql only holds for initdb's connection; store.Open never turns enforcement on, so load and merge write without it. data/caves.db already has passages whose station was deleted by merge.
