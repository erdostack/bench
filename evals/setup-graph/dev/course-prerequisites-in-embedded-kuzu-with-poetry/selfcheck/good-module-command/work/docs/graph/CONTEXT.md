# Graph context

## Facts

engine: Kuzu (embedded, db/courses directory)
engine_version: 0.9.0 (poetry.lock; README says 0.11.3)
query_language: Cypher
driver: kuzu 0.9.0 (Python package)
run_queries: poetry run python -m prereq.cli queries/unreachable.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: prereq/db.py opens db/courses with the kuzu package (embedded, no server)
- engine_version / driver: poetry.lock pins kuzu 0.9.0; the package is the engine, so that is the engine version (pyproject.toml allows >=0.9,<0.12)
- run_queries: Makefile target query -> python -m prereq.cli
- access: make query opens the database read_only=True; make load rebuilds it but nothing authorises an agent to

## Open questions

- README.md says 0.11.3, ahead of the lock (0.9.0).
