# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: bin/q queries/shared_subtier.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: pom.xml property graph.client.version = 6.1.0
- run_queries: bin/q runs AdHocQueryIT through ./mvnw verify, so the failsafe property applies

## Open questions

- None.
