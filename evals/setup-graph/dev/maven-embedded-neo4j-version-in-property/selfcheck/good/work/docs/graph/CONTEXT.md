# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: none (embedded; the org.neo4j:neo4j API is used in-process)
run_queries: bin/cypher queries/orphan_terms.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine and engine_version: pom.xml depends on org.neo4j:neo4j at ${graph.engine.version} = 2026.02.2, embedded (DatabaseManagementServiceBuilder in RunCypher.java)
- run_queries: bin/cypher runs RunCypher through exec:java
- access: RunCypher rolls back every transaction; bin/import is the only writer

## Open questions

- README.md says embedded Neo4j 5.26 LTS, but pom.xml has 2026.02.2 (the 0.8.0 changelog entry upgraded the engine). README is out of date.
