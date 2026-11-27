# How the graph is set up

## Facts

engine: neo4j
engine_version: 2026.09.0 (graphdb.image.tag in the umbrella chart's values)
query_language: Cypher
driver: neo4j-java-driver 5.28.1 (pom.xml ${driver.version})
run_queries: ./mvnw -q exec:java -Dexec.args=queries/dealers_in_common.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/stack/values.yaml sets graphdb.image.tag 2026.09.0, overriding deploy/charts/graphdb/values.yaml (5.26.25); make deploy installs deploy/stack
- driver: pom.xml property driver.version = 5.28.1
- run_queries: bin/query (exec:java, org.atlas.Query, read routing)

## Open questions

- deploy/charts/graphdb/Chart.yaml still says appVersion 5.26.25; the README follows it.
