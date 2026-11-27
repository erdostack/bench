# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: ./gradlew cypher -Pfile=queries/hive_reach.cypher
access: read-write
schema_snapshot: none

## Evidence

- driver: build.gradle.kts, org.neo4j.driver:neo4j-java-driver:6.1.0
- run_queries: build.gradle.kts task cypher
- access: you said writes are fine on the kind database (make reset rebuilds it)

## Open questions

- None.
