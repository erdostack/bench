# Graph context

## Facts

engine: Memgraph (kustomize, lab overlay)
engine_version: 3.5.0 (patched in deploy/overlays/lab; base says 3.2.0)
query_language: Cypher
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/spliceq queries/premises_behind_joint.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `deploy` applies deploy/overlays/lab; its patch memgraph-image.yaml sets the memgraph container's image to memgraph/memgraph:3.5.0 over the base's 3.2.0
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/spliceq (after make forward)
- access: nothing authorises writes

## Open questions

- README.md says Memgraph 3.2.0 (deploy/base), but the lab overlay patches the image to 3.5.0.
