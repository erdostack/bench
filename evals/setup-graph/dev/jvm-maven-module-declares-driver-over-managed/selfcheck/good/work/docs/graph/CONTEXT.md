# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: neo4j-java-driver 5.28.1
run_queries: make query F=queries/interchanges.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:5.26.24-community
- driver: query-cli/pom.xml declares neo4j-java-driver with its own version
- run_queries: Makefile target query (exec:java, QueryCli)

## Open questions

- README.md says the driver is 5.20.0 from the root pom's dependencyManagement, but query-cli/pom.xml sets 5.28.1 on the dependency itself, which is what the build uses.
