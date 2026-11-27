# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: cypher
driver: neo4j-java-driver 5.28.1
run_queries: bin/cypher src/main/resources/queries/lineage.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (image neo4j:2025.10.1)
- driver: pom.xml
- run_queries: bin/cypher (org.seedbank.tools.RunQuery through exec:java)
- access: RunQuery reads only; the ledger import is run by the librarian and nothing authorises tools to write
- schema_snapshot: none yet; docs/model.md is a hand-written sketch, not a snapshot

## Open questions

- None.
