# Graph context

## Facts

engine: neo4j
engine_version: 5.26.26
query_language: Cypher 5
driver: neo4j 5.28.1
run_queries: make cq Q=queries/on_loan_now.cypher
access: read-only
schema_snapshot: docs/graph-model/schema-2026-09.txt

## Evidence

- engine_version: ops/compose/graph.yaml runs neo4j:5.26.26-community; the Makefile's COMPOSE variable points `make up` at that file
- query_language: a 5.26 server runs Cypher 5; the application queries in queries/ carry no prefix (tests/test_queries_parse.py checks that)
- driver: poetry.lock resolves neo4j to 5.28.1; Makefile, Dockerfile and .github/workflows/ci.yml all install with Poetry
- run_queries: Makefile target cq (poetry run python -m curio.tools.cq); CHANGELOG.md 0.14.0 says the shell wrapper is gone
- schema_snapshot: docs/graph-model/schema-2026-09.txt, generated from db.schema procedures and SHOW CONSTRAINTS / SHOW INDEXES
- access: curio/graph.py reads by default; the loader is maintainers-only and nothing authorises an agent to write

## Open questions

- README.md is out of date in four places: it says Neo4j 5.20 (running: 5.26.26), tells people to pip install requirements-dev.txt (which pins neo4j 5.23.1; Poetry installs 5.28.1), names ./scripts/run_query.sh (gone) and db/schema.cypher (does not exist).
- docs/onboarding.md (tools/query.py, neo4j==5.14), docs/adr/0002 (4.4 LTS) and CONTRIBUTING.md (`make query`) are stale too.
- queries/drafts/ is written in Cypher 25 for a planned 2026.x server (docs/upgrade-plan.md). Those files do not run on 5.26.
