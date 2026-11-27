# Graph context

## Facts

engine: Neo4j 2026.08.1 community (Helm, deploy/chart)
engine_version: 2026.08.1
query_language: CYPHER_5 (db.query.default_language in deploy/values/dev.yaml)
driver: neo4j-driver 5.28.1
run_queries: tsx src/cypher.ts queries/reports/producer_reach.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/chart/values.yaml image.tag 2026.08.1-community (dev.yaml leaves it)
- query_language: deploy/values/dev.yaml (yarn cluster:up -f) sets db.query.default_language: CYPHER_5, rendered into neo4j.conf by templates/configmap.yaml
- driver: yarn.lock resolves neo4j-driver 5.28.1
- run_queries: package.json script cypher -> tsx src/cypher.ts

## Open questions

- Style guide (docs/query-style.md) asks for Cypher 25; server default is Cypher 5.
