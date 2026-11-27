# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0-community (nightly.yml input)
query_language: Cypher
driver: neo4j-go-driver/v5 5.28.1
run_queries: go run ./cmd/q <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .github/workflows/nightly.yml passes neo4j-image to the reusable .github/workflows/graph-job.yml
- driver: go.mod
- run_queries: Makefile target q (go run ./cmd/q)

## Open questions

- The README's version is stale.
