# Graph context

## Facts

engine: Neo4j (community, Helm chart deploy/chart via Skaffold)
engine_version: 2026.10.0 (skaffold.yaml setValues; values-local.yaml 2026.07.1 and chart 5.26.18 are overridden)
query_language: Cypher (version not fixed by the repo)
driver: neo4j-driver 5.28.1
run_queries: tsx scripts/cypher.ts queries/recipes_one_swap_away.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: skaffold.yaml (npm run dev) deploys deploy/chart with -f deploy/values-local.yaml and setValues image.tag=2026.10.0; --set beats the values file
- driver: package-lock.json resolves neo4j-driver 5.28.1 (package.json ^5.27.0)
- run_queries: package.json script cypher -> tsx scripts/cypher.ts

## Open questions

- README.md / values-local.yaml version (2026.07.1) is stale.
