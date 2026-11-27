# Graph context

## Facts

engine: memgraph
engine_version: 3.5.0
query_language: Cypher (Memgraph dialect)
driver: neo4j-java-driver 5.13.0
run_queries: make q F=queries/session_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image memgraph/memgraph:3.5.0
- driver: project/Dependencies.scala (Versions.bolt), used by build.sbt
- run_queries: Makefile target q (sbt runMain bandgraph.Query)

## Open questions

- none
