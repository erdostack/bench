# Graph context

## Facts

engine: neo4j
engine_version: 5.26
query_language: Cypher
driver: none (embedded; the org.neo4j:neo4j API is used in-process)
run_queries: bin/cypher queries/orphan_terms.cypher
access: read-only
schema_snapshot: none

## Evidence

- run_queries: bin/cypher runs RunCypher through exec:java
- access: RunCypher rolls back every transaction; bin/import is the only writer

## Open questions

- None.
