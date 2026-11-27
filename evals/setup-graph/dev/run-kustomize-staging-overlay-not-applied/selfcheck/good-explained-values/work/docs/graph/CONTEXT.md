# Graph context

## Facts

engine: Neo4j Community (kustomize, local overlay)
engine_version: 2026.05.0-community (base image; local overlay leaves it)
query_language: Cypher
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/loanq queries/net_lenders.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `up` applies deploy/overlays/local (a storage patch only) over deploy/base/statefulset.yaml, image neo4j:2026.05.0-community; README.md agrees
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/loanq (after make forward)
- access: nothing authorises writes

## Open questions

- None.
