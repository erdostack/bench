# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: cypher
driver: neo4j-java-driver (version managed by the parent pom, unknown)
run_queries: bin/cypher queries/overused_pieces.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (image neo4j:2026.02.2)
- driver: core/pom.xml declares neo4j-java-driver without a version; pom.xml imports neo4j-java-driver-bom at versions.graph-client = 5.28.1
- run_queries: bin/cypher (cli module, org.choirbook.cli.RunCypher through exec:java)
- access: GraphClient only has a read path; nothing authorises writes

## Open questions

- None.
