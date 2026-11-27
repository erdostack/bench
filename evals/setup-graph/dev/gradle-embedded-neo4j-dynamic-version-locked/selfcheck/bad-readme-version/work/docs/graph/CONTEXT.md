# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: none (embedded, in-process API)
run_queries: ./gradlew runCypher -Pfile=queries/vegan_swaps.cypher
access: read-write
schema_snapshot: none

## Evidence

- run_queries: build.gradle.kts task runCypher
- access: AGENTS.md allows writes to build/graph-db (rebuilt by ./gradlew seed)

## Open questions

- None.
