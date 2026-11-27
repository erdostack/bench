# Graph context

## Facts

engine: Neo4j, embedded in the JVM
engine_version: 2026.02.2 (from .mvn/maven.config)
query_language: Cypher
driver: org.neo4j:neo4j 2026.02.2
run_queries: bin/cypher queries/most_cited.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .mvn/maven.config passes -Dneo4j.version=2026.02.2 to every build
- run_queries: bin/cypher (RunCypher, read transaction rolled back)

## Open questions

- README.md and the pom property say 5.26.24, but .mvn/maven.config overrides neo4j.version to 2026.02.2 on every build.
