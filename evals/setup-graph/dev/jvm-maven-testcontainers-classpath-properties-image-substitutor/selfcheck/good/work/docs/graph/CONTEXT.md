# Graph context

## Facts

engine: Neo4j (Testcontainers, throwaway)
engine_version: 2026.02.2
query_language: Cypher
driver: neo4j-java-driver 5.28.5
run_queries: bin/q <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine: src/test/java/org/coldchain/it/GraphFixture.java starts a Testcontainers Neo4jContainer; there is no other database
- engine_version: src/test/resources/testcontainers.properties sets image.substitutor=ReleaseLineImages, which replaces any neo4j image with neo4j:2026.02.2-community
- driver: pom.xml neo4j-driver.version 5.28.5
- run_queries: bin/q -> ./mvnw verify -Dit.test=AdHocQueryIT

## Open questions

- README.md / GraphFixture.java name 5.26.24; the substitutor makes it 2026.02.2.
