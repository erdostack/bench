# Graph context

## Facts

engine: neo4j
engine_version: 5.26.25
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: ./gradlew adhoc -Pcypher=queries/crew_clashes.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: gradle.lockfile neo4j-java-driver 6.1.0 (build file 6.+)
- run_queries: build.gradle.kts task adhoc (AdHocQuery against the seeded container)

## Open questions

- None.
