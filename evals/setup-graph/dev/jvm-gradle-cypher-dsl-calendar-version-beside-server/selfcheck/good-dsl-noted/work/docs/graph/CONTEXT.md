# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5 (server 5.26)
driver: neo4j-java-driver 5.28.1 (Cypher-DSL 2025.2.1 builds queries in code)
run_queries: ./gradlew cypher -Pfile=queries/panels.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:5.26.24-community
- driver: gradle.lockfile (Cypher-DSL 2025.2.1 is a query-builder library, not the server)
- run_queries: build.gradle.kts task cypher

## Open questions

- none
