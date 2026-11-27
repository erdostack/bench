# Graph context

## Facts

engine: neo4j
engine_version: 3.5.0
query_language: Cypher (Memgraph dialect)
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew query -Pfile=queries/downstream_of.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine and engine_version: compose.yaml image memgraph/memgraph:3.5.0
- driver: build.gradle.kts neo4j-java-driver:5.+, locked to 5.28.1 in gradle.lockfile (Bolt client)
- run_queries: build.gradle.kts task query

## Open questions

- README.md says Memgraph 2.21 and docs/ops/runbook.md says 2.21.0, but compose.yaml runs 3.5.0. The runbook steps may not match 3.5.
