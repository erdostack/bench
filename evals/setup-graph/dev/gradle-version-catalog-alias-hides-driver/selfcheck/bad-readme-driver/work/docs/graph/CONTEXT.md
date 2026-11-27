# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/changes_at.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.08.1-community
- run_queries: build.gradle.kts task cypher

## Open questions

- None.
