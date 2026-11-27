# How the graph is set up

## Facts

engine: neo4j
engine_version: 5.26.24-community
query_language: Cypher (v5, as on any 5.26 server)
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/headwaters.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml service graph builds docker/neo4j/Dockerfile, FROM neo4j:5.26.24-community; README.md agrees
- driver: gradle.lockfile neo4j-java-driver 5.28.1
- run_queries: build.gradle.kts task cypher

## Open questions

- graph-next is an opt-in trial service; the facts describe the default one.
