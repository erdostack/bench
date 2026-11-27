# Graph context

## Facts

engine: Neo4j
engine_version: 2026.03.1
query_language: Cypher 5 (docs/query-style.md)
driver: org.neo4j.driver:neo4j-java-driver 5.28.9
run_queries: ./gradlew :lineage:cypher -Pfile=queries/descendants.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: compose.yaml
- run_queries: lineage/build.gradle.kts

## Open questions

- None.
