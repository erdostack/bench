# Graph context

## Facts

engine: neo4j
engine_version: 5.26.23
query_language: cypher
driver: org.neo4j.driver:neo4j-java-driver 5.28.1
run_queries: services/recs/bin/cypher <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (recs-graph, image neo4j:5.26.23-community)
- driver: services/recs/build.gradle.kts
- run_queries: services/recs/bin/cypher (cypher-shell in the container)
- access: nothing authorises writes

## Open questions

- This repo has a second graph store: services/lab uses an embedded Kuzu 0.11.3 (services/lab/requirements.txt), queried with `make -C services/lab query`. The Facts above describe the Neo4j behind services/recs only. Which store should agents treat as the default, or should each service get its own context file?
