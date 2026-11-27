# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 25
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/headwaters.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml service graph builds docker/neo4j/Dockerfile, FROM neo4j:5.26.24-community; README.md agrees
- driver: gradle.lockfile neo4j-java-driver 5.28.1
- run_queries: build.gradle.kts task cypher

## Open questions

- compose.yaml also defines graph-next (neo4j:2026.02.2) under the `next` profile, on port 17687; nothing starts it by default. Is an upgrade planned?
