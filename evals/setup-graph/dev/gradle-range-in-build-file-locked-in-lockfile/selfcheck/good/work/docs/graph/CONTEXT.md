# Graph context

## Facts

engine: neo4j
engine_version: 2025.11.2
query_language: Cypher
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/interchanges.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml neo4j:2025.11.2-community
- driver: gradle.lockfile 5.28.1 (build file range [5.20,7.0))
- run_queries: build.gradle.kts task cypher

## Open questions

- docs/upgrade-plan.md plans server 2026.05.0 and driver 6.1.0; not done yet, so the facts describe the current pins.
