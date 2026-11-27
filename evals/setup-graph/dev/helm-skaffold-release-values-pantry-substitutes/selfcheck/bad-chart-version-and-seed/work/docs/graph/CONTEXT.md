# Graph context

## Facts

engine: neo4j
engine_version: 0.4.2
query_language: Cypher
driver: neo4j-driver 5.28.1
run_queries: npm run seed
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: skaffold.yaml (npm run dev) deploys deploy/chart with -f deploy/values-local.yaml and setValues image.tag=2026.10.0; --set beats the values file
- driver: package-lock.json resolves neo4j-driver 5.28.1 (package.json ^5.27.0)
- run_queries: package.json script cypher -> tsx scripts/cypher.ts

## Open questions

- README.md and deploy/values-local.yaml say 2026.07.1; Skaffold sets 2026.10.0, which is what runs.
- Cypher 5 or Cypher 25 default language is not set anywhere in the chart.
