# Graph context

## Facts

engine: Neo4j
engine_version: 3.5.6 (spring boot)
query_language: Cypher
driver: neo4j-java-driver 5.28.9
run_queries: bin/cypher <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine: spring-boot-docker-compose starts the graph when the app boots
- engine_version: build.gradle.kts bootRun sets spring.profiles.active=local; src/main/resources/application-local.properties sets spring.docker.compose.file=infra/compose.local.yaml, image neo4j:2026.06.0-community
- driver: gradle.lockfile neo4j-java-driver 5.28.9
- run_queries: bin/cypher -> ./gradlew bootRun --args=--cypher.file=... -> CypherRunner

## Open questions

- README says 5.26.24
