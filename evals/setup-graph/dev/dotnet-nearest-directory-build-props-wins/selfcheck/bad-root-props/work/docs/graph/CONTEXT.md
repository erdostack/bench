# Graph context

## Facts

engine: memgraph
engine_version: 3.4.0
query_language: Cypher
driver: Neo4j.Driver 5.20.0
run_queries: make q F=queries/common_ancestor.cypher
access: read-write
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image memgraph/memgraph:3.4.0
- driver: src/Directory.Build.props GraphDriverVersion (nearest to src/Glotto.Query; does not import the root one)
- run_queries: Makefile target q
- access: the request allows writes to the scratch Memgraph (make reset)

## Open questions

- none
