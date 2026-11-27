# Graph context

## Facts

engine: memgraph
engine_version: 2.21.0
query_language: Cypher (Memgraph dialect)
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew query -Pfile=queries/downstream_of.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: build.gradle.kts neo4j-java-driver:5.+, locked to 5.28.1 in gradle.lockfile (Bolt client)
- run_queries: build.gradle.kts task query

## Open questions

- None.
