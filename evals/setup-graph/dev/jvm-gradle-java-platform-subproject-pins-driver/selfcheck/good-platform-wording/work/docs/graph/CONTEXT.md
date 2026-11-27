# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: neo4j-java-driver 6.1.0 (via the :platform java-platform)
run_queries: ./gradlew :query:run --args=queries/review_paths.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.08.1-community
- driver: platform/build.gradle.kts constraint, imported by query/build.gradle.kts
- run_queries: query/build.gradle.kts application plugin

## Open questions

- README.md says neo4j-java-driver 5.28.1; the platform subproject pins 6.1.0.
