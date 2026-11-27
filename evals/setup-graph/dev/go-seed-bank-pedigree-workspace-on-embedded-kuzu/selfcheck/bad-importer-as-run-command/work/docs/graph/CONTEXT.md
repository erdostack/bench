# Graph context

## Facts

engine: kuzu
engine_version: 0.11.3
query_language: Cypher
driver: github.com/kuzudb/go-kuzu v0.11.3
run_queries: make import
access: read-only
schema_snapshot: schema/pedigree.cypher

## Evidence

- engine: pedigree/cmd/lineage/main.go opens data/pedigree.kz with go-kuzu (embedded, no server)
- engine_version / driver: go.work replaces go-kuzu v0.10.0 (pedigree/go.mod) with v0.11.3; make q runs inside the workspace
- run_queries: Makefile target q

## Open questions

- README.md and both go.mod files say go-kuzu / Kuzu 0.10.0; the go.work replace means 0.11.3 is what builds.
