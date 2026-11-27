# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: bin/q queries/who_can.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: src/test/java/org/gatekeeper/support/GraphFixture.java starts neo4j:2026.05.0-community through Testcontainers; there is no compose file or Dockerfile
- driver: pom.xml, org.neo4j.driver:neo4j-java-driver at ${graph.client.version} = 6.1.0
- run_queries: bin/q runs AdHocQuery through ./mvnw against the seeded fixture container
- schema_snapshot: none; src/test/resources/seed.cypher creates the constraints and docs/model.md describes the model
- access: Graph.read routes every query as a read; nothing authorises writes

## Open questions

- None.
