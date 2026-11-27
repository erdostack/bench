# Graph context

## Facts

engine: neo4j
engine_version: 2026.09.0
query_language: cypher
driver: neo4j-driver 6.0.1
run_queries: npm run cypher -- cypher/top_predators.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.override.yaml sets image neo4j:2026.09.0-enterprise; `docker compose up` (npm run db:up, also in CI) merges it over compose.yaml, whose 5.26.25-community is therefore not what runs
- driver: package-lock.json (package.json: ^6.0.0)
- run_queries: package.json script cypher (scripts/cypher.ts)
- access: the runner reads only; the seed script writes, but nothing authorises an agent to

## Open questions

- compose.yaml alone (docker compose -f compose.yaml up) would start 5.26.25-community instead. Is anything still run that way?
