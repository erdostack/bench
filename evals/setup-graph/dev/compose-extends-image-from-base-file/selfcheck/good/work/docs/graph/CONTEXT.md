# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: bin/cypher queries/recall_scope.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml's graph service extends compose.base.yaml (service neo4j), image neo4j:2026.02.2-enterprise
- driver: pom.xml, neo4j-java-driver at ${graph.client.version} = 6.1.0
- run_queries: bin/cypher runs RunQuery through ./mvnw exec:java
- access: RunQuery routes as READ; nothing authorises writes

## Open questions

- README.md says Neo4j 2025.10 and docs/architecture.md says 2025.10.1, but the image that runs comes from compose.base.yaml and is 2026.02.2. The docs are stale.
