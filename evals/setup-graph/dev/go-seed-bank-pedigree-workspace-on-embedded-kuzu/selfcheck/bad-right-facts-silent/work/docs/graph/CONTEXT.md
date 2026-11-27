# Graph context

## Facts

engine: kuzu
engine_version: 0.11.3
query_language: Cypher
driver: github.com/kuzudb/go-kuzu v0.11.3
run_queries: make q F=queries/ancestors.cypher ID=ACC-00412
access: read-only
schema_snapshot: schema/pedigree.cypher

## Evidence

- engine: pedigree/cmd/lineage/main.go opens data/pedigree.kz with go-kuzu (embedded, no server)

## Open questions

- none
