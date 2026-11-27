# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher 5
driver: neo4j-driver 5.28.1
run_queries: yarn cypher queries/recall_reach.cypher --param lot=L-2291
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/chart/values.yaml image.tag 2026.08.1-community (dev.yaml leaves it)
- query_language: deploy/values/dev.yaml (yarn cluster:up -f) sets db.query.default_language: CYPHER_5, rendered into neo4j.conf by templates/configmap.yaml
- driver: yarn.lock resolves neo4j-driver 5.28.1
- run_queries: package.json script cypher -> tsx src/cypher.ts

## Open questions

- docs/query-style.md says the team writes Cypher 25 (LET, FILTER), but the dev server defaults to Cypher 5; queries/recall_reach.cypher uses LET and needs a `CYPHER 25` prefix to run there.
