# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: bin/cypher queries/recall_scope.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: pom.xml, neo4j-java-driver at ${graph.client.version} = 6.1.0
- run_queries: bin/cypher runs RunQuery through ./mvnw exec:java
- access: RunQuery routes as READ; nothing authorises writes

## Open questions

- None.
