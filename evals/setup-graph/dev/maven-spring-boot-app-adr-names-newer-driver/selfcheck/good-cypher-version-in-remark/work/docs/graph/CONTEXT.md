# How the graph is set up

## Facts

engine: neo4j
engine_version: 5.26.26
query_language: Cypher (version 5: the server is the 5.26 LTS line)
driver: org.neo4j.driver:neo4j-java-driver 5.28.1 (graph-driver.version)
run_queries: scripts/cypher.sh queries/lendable_editions.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:5.26.26-community
- driver: pom.xml dependencyManagement, neo4j-java-driver ${graph-driver.version} = 5.28.1 (overrides the Spring Boot parent)
- run_queries: scripts/cypher.sh (cypher-shell in the container, read access mode)
- schema_snapshot: db/schema.cypher (constraints and index, applied on start-up)

## Open questions

- ADR 0004 (Accepted) names driver 6.1.0; the build is still on 5.28.1.
