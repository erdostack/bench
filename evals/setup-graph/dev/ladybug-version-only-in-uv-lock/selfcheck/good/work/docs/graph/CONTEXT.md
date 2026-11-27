# Graph context

## Facts

engine: ladybugdb
engine_version: 0.22.3
query_language: cypher
driver: ladybug 0.22.3
run_queries: just query queries/read_first.cypher
access: read-only
schema_snapshot: src/citeweb/tables.cypher

## Evidence

- engine: README.md and src/citeweb/store.py (import ladybug)
- engine_version, driver: uv.lock resolves ladybug to 0.22.3; pyproject.toml lists it with no version. Embedded, so the package version is the engine version
- run_queries: justfile recipe `query` (python -m citeweb.query)
- schema_snapshot: src/citeweb/tables.cypher holds the table DDL
- access: the query module opens the database read-only; nothing authorises writes

## Open questions

- None.
