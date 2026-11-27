# Graph context

## Facts

engine: Kuzu (embedded, in-process)
engine_version: 0.10
query_language: Cypher
driver: kuzu 0.10
run_queries: make q F=queries/ancestors.cypher
access: read-only
schema_snapshot: schema/stemma.cypher

## Evidence

- run_queries: Makefile target q
- schema_snapshot: schema/stemma.cypher

## Open questions

- none
