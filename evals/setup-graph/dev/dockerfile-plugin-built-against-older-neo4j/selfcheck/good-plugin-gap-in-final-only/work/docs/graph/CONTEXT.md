# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.05.0 (enterprise image, final stage of docker/neo4j/Dockerfile)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.1 (app module)
run_queries: scripts/run-query.sh queries/orphan_depots.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: docker/neo4j/Dockerfile, final stage FROM neo4j:2026.05.0-enterprise; compose.yaml builds that file
- driver: app/pom.xml, neo4j-java-driver 5.28.1
- run_queries: scripts/run-query.sh runs the app module's Query class via exec:java
- access: Query routes as READ

## Open questions

- plugin/pom.xml builds the procedures against 5.26.24; is that intended for a 2026.05.0 server?
