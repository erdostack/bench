# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: python -m foodshare.query queries/single_depot_pantries.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .github/workflows/nightly-report.yml service container neo4j:2026.05.0-community; no compose file or Dockerfile in the repo
- driver: requirements.txt pins neo4j==5.28.1 (installed by the workflow)
- run_queries: foodshare/query.py (one file); the nightly job runs foodshare.report on queries/
- access: nothing authorises writes; foodshare.load is the CI loader

## Open questions

- README.md says Neo4j 5.26, but the only server the repo starts (the CI service container) is 2026.05.0. A Neo4j started by hand may be anything.
