# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher 25
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/fan_in.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: build.gradle.kts 5.+, gradle.lockfile 5.28.1
- run_queries: build.gradle.kts task cypher

## Open questions

- None.
