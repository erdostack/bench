# Graph context

## Facts

engine: memgraph
engine_version: 3.5.0
query_language: Cypher (Memgraph dialect)
driver: neo4j-java-driver 1.11.7
run_queries: make q F=queries/session_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image memgraph/memgraph:3.5.0
- driver: project/Dependencies.scala (Versions.bolt), used by build.sbt
- run_queries: Makefile target q (sbt runMain bandgraph.Query)

## Open questions

- README.md says Neo4j Java driver 5.13.0; project/Dependencies.scala pins 5.28.1.
