# Graph context

## Facts

engine: neo4j (community, started by spring-boot-docker-compose)
engine_version: 2026.06.0-community (infra/compose.local.yaml via the local profile)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.9
run_queries: ./gradlew -q bootRun --args="--cypher.file=queries/lenders_within_two_hops.cypher"
access: read-only
schema_snapshot: none

## Evidence

- engine: spring-boot-docker-compose starts the graph when the app boots
- engine_version: build.gradle.kts bootRun sets spring.profiles.active=local; src/main/resources/application-local.properties sets spring.docker.compose.file=infra/compose.local.yaml, image neo4j:2026.06.0-community
- driver: gradle.lockfile neo4j-java-driver 5.28.9
- run_queries: bin/cypher -> ./gradlew bootRun --args=--cypher.file=... -> CypherRunner

## Open questions

- compose.yaml (and the README) still name 5.26.24.
