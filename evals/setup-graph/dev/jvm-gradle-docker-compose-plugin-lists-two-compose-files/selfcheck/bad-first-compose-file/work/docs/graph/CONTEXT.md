# Graph context

## Facts

engine: Memgraph (Bolt, via the Neo4j Java driver)
engine_version: 2.21.0
query_language: Cypher (Memgraph openCypher)
driver: neo4j-java-driver 5.28.5
run_queries: ./gradlew cypher -Pfile=<file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- compose.yaml: memgraph/memgraph:2.21.0

## Open questions

- none
