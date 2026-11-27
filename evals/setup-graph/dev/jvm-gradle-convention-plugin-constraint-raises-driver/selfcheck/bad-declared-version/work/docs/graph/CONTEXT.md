# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher
driver: neo4j-java-driver 5.20.0
run_queries: ./gradlew :app:cypher -Pfile=queries/busiest_sites.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2025.10.1-community
- driver: buildSrc/src/main/kotlin/stopover.java-conventions.gradle.kts constraint (highest version wins)
- run_queries: app/build.gradle.kts task cypher

## Open questions

- none
