# Graph context

## Facts

engine: neo4j (embedded)
engine_version: 5.26.24 (forced; 2026.05.0 declared)
query_language: Cypher 5 (embedded 5.26 engine)
driver: org.neo4j:neo4j 5.26.24 (embedded)
run_queries: ./gradlew cypher -Pfile=queries/transpositions.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: build.gradle.kts resolutionStrategy force(org.neo4j:neo4j:5.26.24)
- run_queries: build.gradle.kts task cypher (rolls back)

## Open questions

- README.md says embedded Neo4j 2026.05.0 (the declared dependency), but force() holds the engine at 5.26.24 until the store migration; write Cypher 5.
