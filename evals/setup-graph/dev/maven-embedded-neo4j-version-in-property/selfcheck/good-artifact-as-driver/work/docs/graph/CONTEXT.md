# How the graph is set up

## Facts

engine: Neo4j (embedded, no server)
engine_version: 2026.02.2 (graph.engine.version in pom.xml)
query_language: Cypher
driver: org.neo4j:neo4j 2026.02.2 (embedded engine, no Bolt driver)
run_queries: bin/cypher queries/orphan_terms.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine and engine_version: pom.xml depends on org.neo4j:neo4j at ${graph.engine.version} = 2026.02.2, embedded (DatabaseManagementServiceBuilder in RunCypher.java)
- run_queries: bin/cypher runs RunCypher through exec:java
- access: RunCypher rolls back every transaction; bin/import is the only writer

## Open questions

- The README's "embedded Neo4j 5.26 LTS" predates the 0.8.0 upgrade.
