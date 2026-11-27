# Graph context

## Facts

engine: Memgraph
engine_version: 3.5.0
query_language: Cypher (Memgraph dialect)
driver: org.neo4j.driver:neo4j-java-driver 5.28.1
run_queries: sbt -batch "runMain bandgraph.Query queries/session_chain.cypher"
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image memgraph/memgraph:3.5.0
- driver: project/Dependencies.scala (Versions.bolt), used by build.sbt
- run_queries: Makefile target q (sbt runMain bandgraph.Query)

## Open questions

- README.md says Neo4j Java driver 5.13.0; project/Dependencies.scala pins 5.28.1.
