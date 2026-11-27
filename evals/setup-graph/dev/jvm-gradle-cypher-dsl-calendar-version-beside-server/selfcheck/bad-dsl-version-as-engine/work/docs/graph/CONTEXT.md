# Graph context

## Facts

engine: neo4j
engine_version: 2025.2.1
query_language: Cypher 5
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/panels.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: compose.yaml image neo4j:5.26.24-community
- driver: gradle.lockfile (Cypher-DSL 2025.2.1 is a query-builder library, not the server)
- run_queries: build.gradle.kts task cypher

## Open questions

- none
