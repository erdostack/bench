# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: none (embedded, in-process API)
run_queries: ./gradlew runCypher -Pfile=queries/vegan_swaps.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: build.gradle.kts org.neo4j:neo4j:2026.+, locked to 2026.05.0 in gradle.lockfile; embedded via DatabaseManagementServiceBuilder
- run_queries: build.gradle.kts task runCypher
- access: AGENTS.md allows writes to build/graph-db (rebuilt by ./gradlew seed)

## Open questions

- README.md says embedded Neo4j 2026.02.2; the lockfile has 2026.05.0, so the README is behind.
