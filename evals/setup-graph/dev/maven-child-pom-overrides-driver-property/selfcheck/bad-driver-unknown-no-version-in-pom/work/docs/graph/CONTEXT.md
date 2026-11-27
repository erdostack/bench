# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-java-driver unknown
run_queries: make query Q=queries/grounded_by_recall.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.05.0-community
- driver: build-parent/pom.xml manages neo4j-java-driver at ${neo4j-driver.version} (5.28.1 there), and pom.xml sets that property to 6.1.0, which wins
- run_queries: Makefile target query (exec:java, RunCypher)

## Open questions

- README.md says the driver is 5.28 (managed by build-parent), but this pom overrides the property to 6.1.0.
