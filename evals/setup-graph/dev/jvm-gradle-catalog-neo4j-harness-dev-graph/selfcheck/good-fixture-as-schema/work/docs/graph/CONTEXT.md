# Graph context

## Facts

engine: neo4j
engine_version: 2026.03.1 (neo4j-harness, gradle.lockfile)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.9
run_queries: ./gradlew -q run --args="queries/lineage.cypher lot=L-0412"
access: read-only
schema_snapshot: seed/fixture.cypher

## Evidence

- engine: src/main/kotlin/org/seedswap/DevGraph.kt starts Neo4j in-process with neo4j-harness (Neo4jBuilders)
- engine_version: gradle.lockfile locks org.neo4j.test:neo4j-harness and org.neo4j:neo4j at 2026.03.1 (gradle/libs.versions.toml asks for 2026.+)
- driver: gradle.lockfile locks org.neo4j.driver:neo4j-java-driver 5.28.9
- run_queries: bin/cypher -> ./gradlew run -> DevGraphKt

## Open questions

- Docs drift: README.md still says Neo4j 2025.10.
