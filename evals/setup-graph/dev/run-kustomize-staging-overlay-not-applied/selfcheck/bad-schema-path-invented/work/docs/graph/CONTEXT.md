# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/net_lenders.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: Makefile `up` applies deploy/overlays/local (a storage patch only) over deploy/base/statefulset.yaml, image neo4j:2026.05.0-community; README.md agrees
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/loanq (after make forward)
- access: nothing authorises writes

## Open questions

- Staging (deploy/overlays/staging) runs a newer tag; these facts describe the local cluster the Makefile targets.
