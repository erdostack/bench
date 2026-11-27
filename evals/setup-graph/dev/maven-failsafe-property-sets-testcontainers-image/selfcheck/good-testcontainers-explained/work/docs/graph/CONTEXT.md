# How the graph is set up

## Facts

engine: Neo4j (Testcontainers, throwaway)
engine_version: 2026.08.1 (graph.image from the failsafe config; code fallback 5.26.24)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 6.1.0
run_queries: bin/q queries/shared_subtier.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: pom.xml, maven-failsafe-plugin systemPropertyVariables graph.image = neo4j:2026.08.1-community; GraphContainer.java reads that property (default neo4j:5.26.24-community)
- driver: pom.xml property graph.client.version = 6.1.0
- run_queries: bin/q runs AdHocQueryIT through ./mvnw verify, so the failsafe property applies

## Open questions

- The README still says 5.26 for the test container.
