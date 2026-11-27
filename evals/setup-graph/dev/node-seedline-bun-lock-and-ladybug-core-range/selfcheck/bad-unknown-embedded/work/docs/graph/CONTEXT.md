# Graph context

## Facts

engine: ladybug
engine_version: unknown (embedded; no server version)
query_language: Cypher
driver: @ladybugdb/core 0.22.3
run_queries: bun run query queries/descendants.cypher
access: read-only
schema_snapshot: schema/lineage.cypher

## Evidence

- engine_version and driver: bun.lock resolves @ladybugdb/core@0.22.3 (package.json asks for ^0.21.0); the dev container installs with bun install --frozen-lockfile
- engine: src/db.ts opens data/seedline.lbdb in-process with @ladybugdb/core
- run_queries: package.json script query runs src/query.ts
- schema_snapshot: schema/lineage.cypher

## Open questions

- README.md says LadybugDB 0.21, but bun.lock installs 0.22.3.
