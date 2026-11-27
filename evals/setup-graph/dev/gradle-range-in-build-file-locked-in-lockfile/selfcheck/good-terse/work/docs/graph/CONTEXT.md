# How the graph is set up

## Facts

engine: neo4j
engine_version: 2025.11.2
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.1 (locked)
run_queries: ./gradlew cypher -Pfile=<file>
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml neo4j:2025.11.2-community
- driver: gradle.lockfile 5.28.1 (build file range [5.20,7.0))
- run_queries: build.gradle.kts task cypher

## Open questions

- Nothing conflicting found.
