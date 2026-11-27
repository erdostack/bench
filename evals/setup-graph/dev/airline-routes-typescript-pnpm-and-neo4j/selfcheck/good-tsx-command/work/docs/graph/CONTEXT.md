# Graph context

## Facts

engine: Neo4j Community (Docker)
engine_version: 5.26.24-community
query_language: Cypher, version 5
driver: neo4j-driver 5.27.0 (pnpm-lock.yaml)
run_queries: pnpm run query queries/single_carrier_airports.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: compose.yaml runs neo4j:5.26.24-community
- driver: pnpm-lock.yaml resolves neo4j-driver 5.27.0 (package.json: ^5.12.0; packageManager is pnpm)
- run_queries: package.json script query -> tsx src/query.ts
- access: src/query.ts opens READ sessions; the import lives in another repo
- credentials: NEO4J_AUTH in .env (not copied)

## Open questions

- Driver: README claims 6.0.1, lock has 5.27.0.
