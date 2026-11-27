# Graph context

## Facts

engine: Kuzu (embedded graph database, no server)
engine_version: 0.11.3 (embedded in the driver; pinned in requirements.txt, requirements.in only says kuzu>=0.9)
query_language: Cypher (Kuzu dialect)
driver: kuzu (Python package) 0.11.3
run_queries: python -m pantry.cli query queries/<name>.cypher (opens the DB read-only; DB path from PANTRY_DB, default ./var/pantry.kz; the DB is created by `python -m pantry.cli load data/`)
access: read-only
schema_snapshot: schema/tables.cypher

## Evidence

- engine, engine_version, driver: requirements.txt pins kuzu==0.11.3 (requirements.in only says >=0.9); the engine is embedded, so the package version is the engine version
- run_queries: pantry/cli.py, command `query`
- schema_snapshot: schema/tables.cypher holds the table DDL
- access: the query command opens the database read-only; nothing authorises writes

## Open questions

- Nobody upstream is working on kuzu any more: the project was shut down in October 2025 and 0.11.3 is the last version there will be. A fork called LadybugDB carries it on under different package names. Decide whether to stay pinned or move; until then, query syntax must match 0.11.3, not the fork.
