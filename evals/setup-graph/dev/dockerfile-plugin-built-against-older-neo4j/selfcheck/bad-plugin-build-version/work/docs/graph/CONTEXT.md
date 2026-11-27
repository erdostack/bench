# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: neo4j-java-driver 5.28.1
run_queries: scripts/run-query.sh queries/orphan_depots.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: app/pom.xml, neo4j-java-driver 5.28.1
- run_queries: scripts/run-query.sh runs the app module's Query class via exec:java
- access: Query routes as READ

## Open questions

- None.
