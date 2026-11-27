# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.05.0 (locked; build file asks for 2026.+)
query_language: Cypher
driver: org.neo4j:neo4j 2026.05.0 (embedded engine, no network driver)
run_queries: ./gradlew runCypher -Pfile=<file.cypher>
access: read-write
schema_snapshot: none

## Evidence

- engine_version: build.gradle.kts org.neo4j:neo4j:2026.+, locked to 2026.05.0 in gradle.lockfile; embedded via DatabaseManagementServiceBuilder
- run_queries: build.gradle.kts task runCypher
- access: AGENTS.md allows writes to build/graph-db (rebuilt by ./gradlew seed)

## Open questions

- The README names 2026.02.2; gradle.lockfile has moved on to 2026.05.0.
