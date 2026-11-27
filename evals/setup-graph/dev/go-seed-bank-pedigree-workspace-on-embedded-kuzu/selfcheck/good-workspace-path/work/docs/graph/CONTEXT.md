# Graph context

## Facts

engine: Kuzu (embedded via the Go binding)
engine_version: 0.11.3 (go.work replace)
query_language: Cypher
driver: go-kuzu 0.11.3
run_queries: cd pedigree && go run ./cmd/lineage -db ../data/pedigree.kz -f ../queries/shared_parents.cypher id=ACC-00412
access: read-only
schema_snapshot: none

## Evidence

- engine: pedigree/cmd/lineage/main.go opens data/pedigree.kz with go-kuzu (embedded, no server)
- engine_version / driver: go.work replaces go-kuzu v0.10.0 (pedigree/go.mod) with v0.11.3; make q runs inside the workspace
- run_queries: Makefile target q

## Open questions

- pedigree/go.mod still requires 0.10.0; the workspace overrides it.
