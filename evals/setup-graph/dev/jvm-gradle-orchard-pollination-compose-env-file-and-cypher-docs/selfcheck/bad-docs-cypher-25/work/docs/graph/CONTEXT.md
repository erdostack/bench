# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher 25
driver: neo4j-java-driver 5.28.1
run_queries: scripts/q.sh queries/shared_visitors.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: compose.yaml image neo4j:2026.08.1-community
- driver: gradle.lockfile locks org.neo4j.driver:neo4j-java-driver 5.28.1 (build.gradle.kts asks for 5.+)
- run_queries: scripts/q.sh runs ./gradlew -q run --args=<file>
- credentials: graph.env (not copied)

## Open questions

- None.
