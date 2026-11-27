# Graph context

## Facts

engine: neo4j
engine_version: 3.9 (maven:3.9-eclipse-temurin-21)
query_language: Cypher
driver: neo4j-java-driver 5.28.1
run_queries: scripts/run-query.sh queries/orphan_depots.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: docker/neo4j/Dockerfile, final stage FROM neo4j:2026.05.0-enterprise; compose.yaml builds that file
- driver: app/pom.xml, neo4j-java-driver 5.28.1
- run_queries: scripts/run-query.sh runs the app module's Query class via exec:java
- access: Query routes as READ

## Open questions

- The procedures in plugin/ compile against org.neo4j:neo4j 5.26.24 and docs/design/procedures.md says they were built and tested against 5.26.24, but the server they are copied into is 2026.05.0. Have they been tested on 2026.05.0?
