# Graph context

## Facts

engine: Neo4j (in the bagtrace-dev namespace)
engine_version: 2026.08.1-community
query_language: Cypher (default language not set anywhere in the repo)
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/bagq -f queries/slowest_sorters.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: deploy/base/statefulset.yaml (neo4j image), cmd/bagq/main.go
- engine_version: Makefile `up` applies deploy/overlays/dev; it includes deploy/components/calver, whose images entry sets neo4j to 2026.08.1-community
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/bagq

## Open questions

- README says 5.26.24 LTS.
