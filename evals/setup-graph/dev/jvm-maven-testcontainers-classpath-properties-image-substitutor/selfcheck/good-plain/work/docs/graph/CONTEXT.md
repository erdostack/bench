# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2-community (ReleaseLineImages substitutor)
query_language: Cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.5
run_queries: ./mvnw -q verify -Dit.test=AdHocQueryIT -Dcypher.file=queries/longest_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: src/test/java/org/coldchain/it/GraphFixture.java starts a Testcontainers Neo4jContainer; there is no other database
- engine_version: src/test/resources/testcontainers.properties sets image.substitutor=ReleaseLineImages, which replaces any neo4j image with neo4j:2026.02.2-community
- driver: pom.xml neo4j-driver.version 5.28.5
- run_queries: bin/q -> ./mvnw verify -Dit.test=AdHocQueryIT

## Open questions

- README says Neo4j 5.26 LTS; that is the tag the fixture asks for, not the one that starts.
