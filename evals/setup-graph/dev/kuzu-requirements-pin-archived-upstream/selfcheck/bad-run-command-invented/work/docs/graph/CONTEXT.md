# Graph context

## Facts

engine: kuzu
engine_version: 0.11.3
query_language: cypher (Kuzu's dialect)
driver: kuzu 0.11.3
run_queries: ./scripts/kuzu_shell.sh queries/almost_cookable.cypher
access: read-only
schema_snapshot: schema/tables.cypher

## Evidence

- engine, engine_version, driver: requirements.txt pins kuzu==0.11.3 (requirements.in only says >=0.9); the engine is embedded, so the package version is the engine version
- run_queries: pantry/cli.py, command `query`
- schema_snapshot: schema/tables.cypher holds the table DDL
- access: the query command opens the database read-only; nothing authorises writes

## Open questions

- kuzu was archived upstream in October 2025.
