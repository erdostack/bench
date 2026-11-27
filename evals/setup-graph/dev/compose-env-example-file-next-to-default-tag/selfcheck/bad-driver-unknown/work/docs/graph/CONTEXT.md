# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-java-driver unknown (no version in the dependency)
run_queries: bin/cypher queries/orphan_pages.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml neo4j:${NEO4J_TAG:-2026.05.0}-community; .env.example only sets NEO4J_AUTH (NEO4J_TAG commented out); README.md agrees
- driver: pom.xml imports neo4j-java-driver-bom ${graph-bom.version} = 6.1.0
- run_queries: bin/cypher (exec:java)

## Open questions

- If someone uncomments NEO4J_TAG in their own .env the local server changes; the repo default is 2026.05.0.
