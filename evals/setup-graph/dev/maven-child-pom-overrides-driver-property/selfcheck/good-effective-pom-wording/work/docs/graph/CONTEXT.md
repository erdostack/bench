# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 6.1.0 (effective version; property overridden in pom.xml)
run_queries: ./mvnw -q exec:java -Dexec.args=queries/depots_for_bogie.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.05.0-community
- driver: build-parent/pom.xml manages neo4j-java-driver at ${neo4j-driver.version} (5.28.1 there), and pom.xml sets that property to 6.1.0, which wins
- run_queries: Makefile target query (exec:java, RunCypher)

## Open questions

- build-parent still pins 5.28.1 for its other users; this project has moved past it.
