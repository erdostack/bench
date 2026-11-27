# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: neo4j-driver 6.0.1
run_queries: npm run cq -- queries/where_used.cypher part=BRK-220
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/values/dev.yaml
- driver: package-lock.json resolves neo4j-driver to 6.0.1 (package.json: ^6.0.0)
- run_queries: package.json script cq (tsx tools/cq.ts)
- schema_snapshot: docs/model.md describes the model in prose; there is no dump
- access: tools/cq.ts runs read transactions; nothing authorises writes

## Open questions

- None.
