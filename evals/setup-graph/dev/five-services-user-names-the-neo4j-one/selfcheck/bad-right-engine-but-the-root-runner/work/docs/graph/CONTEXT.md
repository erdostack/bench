# Graph context

## Facts

engine: neo4j
engine_version: 2026.09.0
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: make mgq FILE=services/lineage/queries/upstream_of.cypher
access: read-only
schema_snapshot: services/lineage/schema/constraints.cypher

## Evidence

- engine, engine_version: services/lineage/dev/compose.yaml runs neo4j:2026.09.0-community; services/lineage/README.md says the service brings its own database
- driver: services/lineage/gradle.lockfile resolves org.neo4j.driver:neo4j-java-driver to 6.1.0 (build.gradle.kts: 6.+)
- run_queries: services/lineage/bin/lq wraps ./gradlew runQuery (io.tidepool.lineage.RunQuery)
- schema_snapshot: services/lineage/schema/constraints.cypher lists the constraints; there is no full dump
- access: LineageGraph only runs read queries and the README says to treat the database as read; nothing authorises writes

## Open questions

- The root README.md and docs/architecture.md describe Memgraph 3.5 as the platform's graph database, and the architecture notes say lineage will share it. That is not what services/lineage does today: it runs its own Neo4j. The Memgraph instance belongs to services/routing.
- Nothing in the repo shows whether the lineage database runs Cypher 5 or Cypher 25 by default.
