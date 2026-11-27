# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-driver 5.28.1
run_queries: npm run q -- queries/reachable_in_20.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: docker-bake.hcl
- driver: package-lock.json

## Open questions

- none
