# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: neo4j-driver 5.28.1
run_queries: npm run q -- queries/skill_chains.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .devcontainer/devcontainer.json uses dockerComposeFile [../compose.yaml, compose.devcontainer.yaml]; the second file overrides the graph image with neo4j:2026.02.2-community (compose.yaml alone says 5.26.24)
- driver: package-lock.json resolves neo4j-driver 5.28.1
- run_queries: package.json script q runs tsx src/q.ts
- access: nothing authorises writes

## Open questions

- README.md says Neo4j 5.26.24 (compose.yaml), but the dev container, which README.md says starts the graph, runs 2026.02.2.
