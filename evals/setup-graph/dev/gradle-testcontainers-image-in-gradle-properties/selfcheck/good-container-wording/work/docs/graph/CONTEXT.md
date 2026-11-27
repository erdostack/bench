# How the graph is set up

## Facts

engine: Neo4j Enterprise (Testcontainers)
engine_version: 2026.09.0-enterprise (graphImage in gradle.properties)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 6.1.0
run_queries: ./gradlew adhoc -Pcypher=queries/crew_clashes.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: gradle.properties graphImage=neo4j:2026.09.0-enterprise, passed as graph.image to every Test task by build.gradle.kts; GraphFixture.java falls back to neo4j:5.26.25 only without it
- driver: gradle.lockfile neo4j-java-driver 6.1.0 (build file 6.+)
- run_queries: build.gradle.kts task adhoc (AdHocQuery against the seeded container)

## Open questions

- README (and GraphFixture's fallback) still name 5.26.25.
