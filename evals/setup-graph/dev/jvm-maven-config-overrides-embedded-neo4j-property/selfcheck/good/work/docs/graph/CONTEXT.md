# Graph context

## Facts

engine: neo4j (embedded)
engine_version: 2026.02.2
query_language: Cypher
driver: none (embedded API, org.neo4j:neo4j 2026.02.2)
run_queries: bin/cypher queries/most_cited.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .mvn/maven.config passes -Dneo4j.version=2026.02.2 to every build
- run_queries: bin/cypher (RunCypher, read transaction rolled back)

## Open questions

- README.md and the pom property say 5.26.24, but .mvn/maven.config overrides neo4j.version to 2026.02.2 on every build.
