# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make forward
access: read-only
schema_snapshot: none

## Evidence

- engine: deploy/base/statefulset.yaml (neo4j image), cmd/bagq/main.go
- engine_version: Makefile `up` applies deploy/overlays/dev; it includes deploy/components/calver, whose images entry sets neo4j to 2026.08.1-community
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/bagq

## Open questions

- README.md and deploy/base/statefulset.yaml say 5.26.24; the dev overlay's calver component retags the image to 2026.08.1.
