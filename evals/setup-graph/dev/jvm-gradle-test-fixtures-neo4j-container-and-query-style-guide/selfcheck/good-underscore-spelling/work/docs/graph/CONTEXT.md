# Graph context

## Facts

engine: neo4j
engine_version: 2026.04.0-community
query_language: CYPHER_5 (db.query.default_language in GraphServer)
driver: org.neo4j.driver:neo4j-java-driver 6.0.2
run_queries: ./gradlew -q adhoc -Pcypher=queries/tight_connections.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: src/testFixtures/java/org/crewpair/fixtures/GraphServer.java starts neo4j:2026.04.0-community with Testcontainers
- query_language: the same fixture sets db.query.default_language=CYPHER_5 (withNeo4jConfig)
- driver: gradle.lockfile neo4j-java-driver 6.0.2 (build.gradle.kts: 6.+)
- run_queries: bin/q -> ./gradlew adhoc -Pcypher=<file> -> AdHocQueryTest

## Open questions

- query-style.md assumes Cypher 25.
