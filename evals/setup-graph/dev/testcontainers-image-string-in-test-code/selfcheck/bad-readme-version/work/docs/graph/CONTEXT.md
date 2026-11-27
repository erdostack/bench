# Graph context

## Facts

engine: neo4j
engine_version: 5.26
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: bin/q queries/who_can.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: README.md (Requirements)
- driver: pom.xml, org.neo4j.driver:neo4j-java-driver at ${graph.client.version} = 6.1.0
- run_queries: bin/q runs AdHocQuery through ./mvnw against the seeded fixture container
- schema_snapshot: none; src/test/resources/seed.cypher creates the constraints and docs/model.md describes the model
- access: Graph.read routes every query as a read; nothing authorises writes

## Open questions

- None.
