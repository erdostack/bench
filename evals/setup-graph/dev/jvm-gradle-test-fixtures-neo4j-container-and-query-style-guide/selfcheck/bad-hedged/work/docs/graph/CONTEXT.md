# Graph context

## Facts

engine: Neo4j (Testcontainers)
engine_version: 2026.04.0
query_language: Cypher 5 or 25
driver: neo4j-java-driver 6.0.2
run_queries: bin/q <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: src/testFixtures/java/org/crewpair/fixtures/GraphServer.java starts neo4j:2026.04.0-community with Testcontainers
- query_language: the same fixture sets db.query.default_language=CYPHER_5 (withNeo4jConfig)
- driver: gradle.lockfile neo4j-java-driver 6.0.2 (build.gradle.kts: 6.+)
- run_queries: bin/q -> ./gradlew adhoc -Pcypher=<file> -> AdHocQueryTest

## Open questions

- none
