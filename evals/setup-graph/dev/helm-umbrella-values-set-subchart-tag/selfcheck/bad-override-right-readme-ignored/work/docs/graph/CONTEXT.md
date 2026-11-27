# Graph context

## Facts

engine: neo4j
engine_version: 2026.09.0
query_language: Cypher
driver: neo4j-java-driver 5.28.1
run_queries: bin/query queries/gaps_in_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: pom.xml property driver.version = 5.28.1
- run_queries: bin/query (exec:java, org.atlas.Query, read routing)

## Open questions

- None.
