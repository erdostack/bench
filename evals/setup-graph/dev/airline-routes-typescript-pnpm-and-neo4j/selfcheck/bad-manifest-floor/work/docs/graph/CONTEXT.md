# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: neo4j-driver ^5.12.0
run_queries: pnpm query queries/one_stop.cypher from=LIS to=OSL
access: read-only
schema_snapshot: schema/schema.cypher

## Evidence

- engine / engine_version: compose.yaml runs neo4j:5.26.24-community
- driver: pnpm-lock.yaml resolves neo4j-driver 5.27.0 (package.json: ^5.12.0; packageManager is pnpm)
- run_queries: package.json script query -> tsx src/query.ts
- access: src/query.ts opens READ sessions; the import lives in another repo
- credentials: NEO4J_AUTH in .env (not copied)

## Open questions

- README.md lists neo4j-driver 6.0.1, but pnpm-lock.yaml installs 5.27.0, and package.json's ^5.12.0 cannot reach 6.x. The README is wrong about the driver.
