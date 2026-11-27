# Graph context

## Facts

engine: neo4j (compose service lineage)
engine_version: 2026.03.1-community
query_language: CYPHER_25 (db.query.default_language set in compose.yaml)
driver: neo4j-java-driver 5.28.9
run_queries: ./gradlew :lineage:cypher -Pfile=queries/lines_without_recent_regrow.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine and engine_version: compose.yaml service lineage, neo4j:2026.03.1-community
- query_language: the same service sets NEO4J_db_query_default__language: CYPHER_25 (db.query.default_language)
- driver: lineage/gradle.lockfile neo4j-java-driver 5.28.9 (build file asks for 5.+)
- run_queries: lineage/build.gradle.kts task cypher -> org.seedvault.lineage.Cypher

## Open questions

- docs/query-style.md says the lineage database runs Cypher 5 and asks for Cypher 5 queries, but compose.yaml makes Cypher 25 the default language. Either the guide or the compose setting should change; queries can also pin a version with a `CYPHER 5` prefix.
