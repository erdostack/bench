# Graph context

## Facts

engine: neo4j
engine_version: 5.26.23
query_language: cypher
driver: kuzu 0.11.3
run_queries: make -C services/lab query
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (recs-graph, image neo4j:5.26.23-community)
- driver: services/recs/build.gradle.kts
- run_queries: services/recs/bin/cypher (cypher-shell in the container)
- access: nothing authorises writes

## Open questions

- services/lab uses kuzu
