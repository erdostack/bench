# Graph context

## Facts

engine: ladybug
engine_version: 0.9.0
query_language: Cypher (Kuzu dialect)
driver: ladybug 0.9.0
run_queries: make query F=queries/all_prereqs.cypher CODE=MATH201
access: read-only
schema_snapshot: schema/schema.cypher

## Evidence

- engine: prereq/db.py opens db/courses with the kuzu package (embedded, no server)
- engine_version / driver: poetry.lock pins kuzu 0.9.0; the package is the engine, so that is the engine version (pyproject.toml allows >=0.9,<0.12)
- run_queries: Makefile target query -> python -m prereq.cli
- access: make query opens the database read_only=True; make load rebuilds it but nothing authorises an agent to

## Open questions

- README.md says Kuzu 0.11.3, but poetry.lock installs 0.9.0: either the README was written ahead of an upgrade that never happened, or the lock needs updating.
