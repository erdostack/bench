# Graph context

## Facts

engine: ladybugdb (embedded)
engine_version: 0.22.3
query_language: cypher (LadybugDB dialect)
driver: @ladybugdb/core 0.22.3
run_queries: npm run lq -w services/atlas -- queries/step_free.cypher
access: read-only
schema_snapshot: services/atlas/schema/tables.cypher

## Evidence

- scope: services/atlas only, as asked
- engine: services/atlas/src/store.mjs imports @ladybugdb/core and opens var/paths.lbug
- engine_version, driver: package-lock.json at the repo root resolves @ladybugdb/core to 0.22.3 (services/atlas/package.json: ^0.22.0)
- run_queries: services/atlas/package.json script lq (bin/lq.mjs)
- access: lq opens the file read-only; only the print pipeline's build-graph writes

## Open questions

- The repo's other graph store, the Neo4j 2025.10.1 in compose.yaml, belongs to services/catalog and is not covered here.
