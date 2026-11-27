# Graph context

## Facts

engine: Memgraph (Docker, compose profile `current`)
engine_version: 3.4.0 (service memgraph-3; the 2.18.1 one is only under --profile legacy)
query_language: Cypher
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/bagq queries/dead_ends.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `up` runs `docker compose --profile current up -d`; only memgraph-3 (memgraph/memgraph:3.4.0) is in that profile, the 2.18.1 service is in `legacy`
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/bagq
- access: nothing authorises writes

## Open questions

- README.md says Memgraph 2.18.1 (the memgraph service), but `make up` starts the current profile, Memgraph 3.4.0. The README is out of date.
