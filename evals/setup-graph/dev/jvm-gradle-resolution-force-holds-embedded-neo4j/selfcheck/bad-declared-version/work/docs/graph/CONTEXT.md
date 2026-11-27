# Graph context

## Facts

engine: neo4j (embedded)
engine_version: 2026.05.0
query_language: Cypher 5
driver: none (embedded Java API)
run_queries: ./gradlew cypher -Pfile=queries/transpositions.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: build.gradle.kts resolutionStrategy force(org.neo4j:neo4j:5.26.24)
- run_queries: build.gradle.kts task cypher (rolls back)

## Open questions

- none
