# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: ./gradlew cypher -Pfile=queries/changes_at.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.08.1-community
- driver: build.gradle.kts implementation(libs.graph.client); gradle/libs.versions.toml maps graph-client to org.neo4j.driver:neo4j-java-driver, version graphClient = 6.1.0
- run_queries: build.gradle.kts task cypher

## Open questions

- README.md says Neo4j Java driver 5.28.1, and gradle.properties still has neo4jDriverVersion=5.28.1, which nothing reads. The build uses 6.1.0 from the version catalog.
