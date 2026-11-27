# Graph context

## Facts

engine: memgraph
engine_version: 3.4.0
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/slowest_transfers.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: Makefile `up` runs `docker compose --profile current up -d`; only memgraph-3 (memgraph/memgraph:3.4.0) is in that profile, the 2.18.1 service is in `legacy`
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/bagq
- access: nothing authorises writes

## Open questions

- README.md says Memgraph 2.18.1 (the memgraph service), but `make up` starts the current profile, Memgraph 3.4.0. The README is out of date.
