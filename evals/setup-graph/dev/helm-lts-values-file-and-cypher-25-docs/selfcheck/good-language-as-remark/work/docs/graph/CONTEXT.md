# How the graph is set up

## Facts

engine: neo4j
engine_version: 5.26.29-enterprise (support.yaml overrides the chart's 2026.08.1)
query_language: Cypher (version 5 on this server)
driver: neo4j-java-driver 5.28.1
run_queries: ./gradlew cypher -Pfile=queries/fan_in.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile deploy passes -f deploy/values/support.yaml (image.tag 5.26.29-enterprise) over deploy/chart/values.yaml (2026.08.1-enterprise); CHANGELOG 2026-09-30
- driver: build.gradle.kts 5.+, gradle.lockfile 5.28.1
- run_queries: build.gradle.kts task cypher

## Open questions

- The README's 2026.08 / Cypher 25 no longer matches what is deployed; the query style guide needs the same fix.
