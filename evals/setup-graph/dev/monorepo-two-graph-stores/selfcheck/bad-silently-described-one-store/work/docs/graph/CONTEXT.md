# Graph context

## Facts

engine: neo4j
engine_version: 5.26.23
query_language: cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.1
run_queries: services/recs/bin/cypher <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (recs-graph, image neo4j:5.26.23-community)
- driver: services/recs/build.gradle.kts
- run_queries: services/recs/bin/cypher (cypher-shell in the container)
- access: nothing authorises writes

## Open questions

- None.
