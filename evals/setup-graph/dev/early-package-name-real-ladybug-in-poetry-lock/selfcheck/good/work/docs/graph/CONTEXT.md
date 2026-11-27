# Graph context

## Facts

engine: LadybugDB
engine_version: 0.12.0
query_language: Cypher
driver: real_ladybug 0.12.0
run_queries: poetry run bandtree-ask queries/shared_members.cypher band="The Quiet Lanterns"
access: read-only
schema_snapshot: schema/tables.cypher

## Evidence

- engine: README.md and bandtree/store.py (import real_ladybug)
- engine_version, driver: poetry.lock resolves real-ladybug to 0.12.0 (pyproject.toml: >=0.12,<0.14). Embedded, so the package version is the engine version
- run_queries: pyproject.toml script bandtree-ask = bandtree.ask:main
- schema_snapshot: schema/tables.cypher is the table DDL the loader runs
- access: bandtree-ask opens the database read-only; nothing authorises writes

## Open questions

- The binding is installed under its early name, real_ladybug. The same library is now published on PyPI as `ladybug` (CONTRIBUTING.md, housekeeping backlog); the repo has not moved yet.
