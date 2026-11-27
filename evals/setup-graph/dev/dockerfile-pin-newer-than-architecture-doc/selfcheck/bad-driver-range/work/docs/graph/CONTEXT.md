# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: cypher
driver: neo4j-driver ^5.25.0
run_queries: pnpm cypher cypher/reissue_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: infra/neo4j/Dockerfile (FROM neo4j:2026.05.0-enterprise), built by compose.yaml
- driver: pnpm-lock.yaml resolves neo4j-driver to 5.27.0 (package.json: ^5.25.0)
- run_queries: package.json script `cypher` (scripts/run-cypher.ts)
- access: the service has no write path and nothing authorises writes
- schema_snapshot: none; infra/neo4j/constraints.cypher lists constraints only

## Open questions

- architecture.md says 5.18; Dockerfile says 2026.05.0
