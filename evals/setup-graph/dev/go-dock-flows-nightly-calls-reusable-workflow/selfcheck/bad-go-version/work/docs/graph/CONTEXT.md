# Graph context

## Facts

engine: Neo4j
engine_version: 1.23
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/drain_chains.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .github/workflows/nightly.yml passes neo4j-image to the reusable .github/workflows/graph-job.yml
- driver: go.mod
- run_queries: Makefile target q (go run ./cmd/q)

## Open questions

- README.md says Neo4j 5.26 and graph-job.yml's input default is 5.26.24; the nightly caller overrides it with 2026.05.0.
