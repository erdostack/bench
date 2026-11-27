# Graph context

## Facts

engine: neo4j
engine_version: 5.26.26
query_language: Cypher 5
driver: neo4j-java-driver 5.28.1
run_queries: scripts/cypher.sh queries/lendable_editions.cypher
access: read-only
schema_snapshot: db/schema.cypher

## Evidence

- engine_version: compose.yaml image neo4j:5.26.26-community
- driver: pom.xml dependencyManagement, neo4j-java-driver ${graph-driver.version} = 5.28.1 (overrides the Spring Boot parent)
- run_queries: scripts/cypher.sh (cypher-shell in the container, read access mode)
- schema_snapshot: db/schema.cypher (constraints and index, applied on start-up)

## Open questions

- docs/adr/0004-driver-6.md is Accepted and says the service moves to neo4j-java-driver 6.1.0, but pom.xml still pins 5.28.1. Either the ADR has not been carried out or the pom was reverted.
