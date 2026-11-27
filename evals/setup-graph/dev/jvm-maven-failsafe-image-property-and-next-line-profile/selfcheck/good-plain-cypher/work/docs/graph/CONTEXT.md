# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24-community (pom graph.image)
query_language: Cypher (the 5.26 line only speaks Cypher 5)
driver: org.neo4j.driver:neo4j-java-driver 5.28.5
run_queries: ./mvnw -q verify -Dit.test=AdHocQueryIT -Dcypher.file=queries/ponds_by_vector.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: pom.xml property graph.image = neo4j:5.26.24-community, passed by failsafe to GraphContainer (Testcontainers)
- the next-line profile (neo4j:2026.08.1-community) is opt-in; bin/q, .github/workflows/ci.yml and .mvn/maven.config do not activate it
- driver: pom.xml neo4j-driver.version 5.28.5
- run_queries: bin/q -> ./mvnw verify -Dit.test=AdHocQueryIT

## Open questions

- none; -Pnext-line would switch to 2026.08.1 but is opt-in.
