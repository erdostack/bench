# How the graph is set up

## Facts

engine: Memgraph (talked to over Bolt with the Neo4j Java driver)
engine_version: 3.5.0
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.1 (gradle.lockfile; build file says 5.+)
run_queries: ./gradlew query -Pfile=queries/downstream_of.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine and engine_version: compose.yaml image memgraph/memgraph:3.5.0
- driver: build.gradle.kts neo4j-java-driver:5.+, locked to 5.28.1 in gradle.lockfile (Bolt client)
- run_queries: build.gradle.kts task query

## Open questions

- The runbook was written for Memgraph 2.21.0; the stack has moved to 3.5.0.
