# Graph context

## Facts

engine: Neo4j (own Helm chart in deploy/chart)
engine_version: 2026.08.1 (GRAPH_TAG passed with --set; beats values-dev.yaml's 2026.05.0)
query_language: Cypher
driver: neo4j-go-driver v5.28.1 (go.mod)
run_queries: go run ./cmd/tq queries/blocked_trams.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `deploy` runs helm with -f deploy/values-dev.yaml (2026.05.0) and then --set image.tag=$(GRAPH_TAG), GRAPH_TAG ?= 2026.08.1; --set wins. Chart default 2026.02.2
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/tq (after make forward)
- access: nothing authorises writes

## Open questions

- README.md says Neo4j 2026.05.0 (deploy/values-dev.yaml), but `make deploy` overrides it with --set image.tag=2026.08.1. Is values-dev.yaml's tag still used anywhere?
