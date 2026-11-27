# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.02.2-enterprise (inherited through `extends` from compose.base.yaml)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 6.1.0
run_queries: ./mvnw -q exec:java -Dexec.args=queries/shared_dye_lots.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml's graph service extends compose.base.yaml (service neo4j), image neo4j:2026.02.2-enterprise
- driver: pom.xml, neo4j-java-driver at ${graph.client.version} = 6.1.0
- run_queries: bin/cypher runs RunQuery through ./mvnw exec:java
- access: RunQuery routes as READ; nothing authorises writes

## Open questions

- README.md (2025.10) and docs/architecture.md (2025.10.1) disagree with compose.base.yaml; compose.base.yaml is copied from the platform repo by hand, so check it is current.
