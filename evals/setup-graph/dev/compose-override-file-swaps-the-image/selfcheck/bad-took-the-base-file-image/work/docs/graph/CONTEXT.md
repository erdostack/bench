# Graph context

## Facts

engine: neo4j
engine_version: 5.26.25-community
query_language: cypher
driver: neo4j-driver 6.0.1
run_queries: npm run cypher -- cypher/top_predators.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml
- driver: package-lock.json (package.json: ^6.0.0)
- run_queries: package.json script cypher (scripts/cypher.ts)
- access: the runner reads only; the seed script writes, but nothing authorises an agent to

## Open questions

- None.
