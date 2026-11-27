# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.05.0-community
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 6.1.0 (BOM import)
run_queries: ./mvnw -q exec:java -Dexec.args=queries/click_path.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml neo4j:${NEO4J_TAG:-2026.05.0}-community; .env.example only sets NEO4J_AUTH (NEO4J_TAG commented out); README.md agrees
- driver: pom.xml imports neo4j-java-driver-bom ${graph-bom.version} = 6.1.0
- run_queries: bin/cypher (exec:java)

## Open questions

- The README and compose.yaml agree; nothing to reconcile.
