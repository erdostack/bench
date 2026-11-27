# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: bin/q queries/shared_subtier.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: pom.xml, maven-failsafe-plugin systemPropertyVariables graph.image = neo4j:2026.08.1-community; GraphContainer.java reads that property (default neo4j:5.26.24-community)
- driver: pom.xml property graph.client.version = 6.1.0
- run_queries: bin/q runs AdHocQueryIT through ./mvnw verify, so the failsafe property applies

## Open questions

- README.md says the tests use Neo4j 5.26, and GraphContainer.java defaults to 5.26.24, but the failsafe config overrides it with 2026.08.1, so every run uses 2026.08.1.
