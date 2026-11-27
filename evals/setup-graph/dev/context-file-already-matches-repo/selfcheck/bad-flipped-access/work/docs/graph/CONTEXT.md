# Graph context

## Facts

engine: postgresql
engine_version: 17.7
query_language: sql (recursive CTEs over the course and prerequisite tables)
driver: psycopg 3.2.9
run_queries: make sql FILE=sql/all_prereqs.sql
access: read-write
schema_snapshot: docs/graph/schema.md

## Evidence

- engine, engine_version: docker-compose.yml (image postgres:17.7)
- query_language: sql/*.sql; docs/adr/0003-no-graph-extension.md records why there is no graph extension
- driver: Pipfile.lock (psycopg ==3.2.9; Pipfile has ~=3.2)
- run_queries: Makefile target sql (psql in the db container, read-only session)
- access: Makefile forces a read-only session; planner/db.py sets read_only; nothing authorises writes
- schema_snapshot: docs/graph/schema.md, taken from sql/schema.sql

## Open questions

- None.
