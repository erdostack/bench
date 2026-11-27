# Graph context

## Facts

engine: neo4j (embedded)
engine_version: 5.26.24
query_language: Cypher
driver: none (embedded API)
run_queries: bin/cypher queries/most_cited.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .mvn/maven.config passes -Dneo4j.version=2026.02.2 to every build
- run_queries: bin/cypher (RunCypher, read transaction rolled back)

## Open questions

- none
