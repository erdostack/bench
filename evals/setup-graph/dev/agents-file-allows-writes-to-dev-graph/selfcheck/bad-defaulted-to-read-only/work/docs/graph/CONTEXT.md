# Graph context

## Facts

engine: neo4j
engine_version: 5.26.29
query_language: cypher
driver: org.neo4j.driver:neo4j-java-driver:5.28.1
run_queries: ./gradlew cypher -Pfile=src/main/resources/cypher/berth_conflicts.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (image neo4j:5.26.29-community)
- driver: gradle.lockfile (build.gradle.kts has the dynamic version 5.+)
- run_queries: build.gradle.kts task `cypher` (dev.dockyard.CypherFile)

## Open questions

- None.
