# Graph context

## Facts

engine: Neo4j (in-process, neo4j-harness; no server)
engine_version: 2026.03.1
query_language: Cypher
driver: neo4j-java-driver 5.28.9
run_queries: bin/cypher <file.cypher> [key=value ...]
access: read-only
schema_snapshot: none

## Evidence

- engine: src/main/kotlin/org/seedswap/DevGraph.kt starts Neo4j in-process with neo4j-harness (Neo4jBuilders)
- engine_version: gradle.lockfile locks org.neo4j.test:neo4j-harness and org.neo4j:neo4j at 2026.03.1 (gradle/libs.versions.toml asks for 2026.+)
- driver: gradle.lockfile locks org.neo4j.driver:neo4j-java-driver 5.28.9
- run_queries: bin/cypher -> ./gradlew run -> DevGraphKt

## Open questions

- README.md says in-process Neo4j 2025.10; gradle.lockfile has neo4j-harness 2026.03.1.
