# Graph context

## Facts

engine: memgraph
engine_version: 3.4.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: make q F=queries/long_rides.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/memgraph/values.yaml has tag "", and templates/statefulset.yaml uses `.Values.image.tag | default .Chart.AppVersion`; Chart.yaml appVersion is 3.4.0
- driver: requirements.txt pins neo4j==5.28.1
- run_queries: Makefile target q runs python -m busroute.query (after make forward)
- access: nothing authorises writes

## Open questions

- README.md says Memgraph 2.21.0, but the chart deploys appVersion 3.4.0. The README is stale.
