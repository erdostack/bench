# Graph context

## Facts

engine: ladybug
engine_version: 0.21
query_language: Cypher
driver: @ladybugdb/core ^0.21.0
run_queries: bun run query queries/descendants.cypher
access: read-only
schema_snapshot: schema/lineage.cypher

## Evidence

- engine: src/db.ts opens data/seedline.lbdb in-process with @ladybugdb/core
- run_queries: package.json script query runs src/query.ts
- schema_snapshot: schema/lineage.cypher

## Open questions

- None.
