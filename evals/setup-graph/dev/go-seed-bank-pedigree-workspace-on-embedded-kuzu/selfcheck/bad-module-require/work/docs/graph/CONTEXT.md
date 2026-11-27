# Graph context

## Facts

engine: kuzu
engine_version: 0.10.0
query_language: Cypher
driver: github.com/kuzudb/go-kuzu v0.10.0
run_queries: make q F=queries/ancestors.cypher ID=ACC-00412
access: read-only
schema_snapshot: schema/pedigree.cypher

## Evidence

- engine_version / driver: pedigree/go.mod, README.md

## Open questions

- none
