# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: CYPHER_5 (db.query.default_language via graph.env)
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew -q run --args=queries/lonely_varieties.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: compose.yaml image neo4j:2026.08.1-community
- query_language: graph.env (the graph service's env_file) sets NEO4J_db_query_default__language=CYPHER_5
- driver: gradle.lockfile locks org.neo4j.driver:neo4j-java-driver 5.28.1 (build.gradle.kts asks for 5.+)
- run_queries: scripts/q.sh runs ./gradlew -q run --args=<file>
- credentials: graph.env (not copied)

## Open questions

- docs/writing-queries.md assumes the 2026.x default (Cypher 25); graph.env overrides it to CYPHER_5.
