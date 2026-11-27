# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 6.1.0 (catalog alias graph-client)
run_queries: ./gradlew cypher -Pfile=<path>
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.08.1-community
- driver: build.gradle.kts implementation(libs.graph.client); gradle/libs.versions.toml maps graph-client to org.neo4j.driver:neo4j-java-driver, version graphClient = 6.1.0
- run_queries: build.gradle.kts task cypher

## Open questions

- gradle.properties has a leftover neo4jDriverVersion=5.28.1 and the README repeats it; the real version is in gradle/libs.versions.toml.
