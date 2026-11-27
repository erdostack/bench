# Graph context

## Facts

engine: neo4j
engine_version: 0.5.0 (chart)
query_language: Cypher 5
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/fan_in.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile deploy passes -f deploy/values/support.yaml (image.tag 5.26.29-enterprise) over deploy/chart/values.yaml (2026.08.1-enterprise); CHANGELOG 2026-09-30
- driver: build.gradle.kts 5.+, gradle.lockfile 5.28.1
- run_queries: build.gradle.kts task cypher

## Open questions

- README.md and docs/query-style.md say Neo4j 2026.08 and Cypher 25, and the chart defaults to 2026.08.1, but deployments run 5.26.29. That server only has Cypher 5, so Cypher 25-only syntax (for example the quantified path pattern in queries/ring_candidates.cypher) will not run there.
