# How the graph is set up

## Facts

engine: Neo4j (Community edition, in Docker)
engine_version: 2026.08.1-community (NEO4J_TAG from .env; the 5.26.24 fallback only applies when it is unset)
query_language: Cypher
driver: neo4j-go-driver v5.28.1 (go.mod)
run_queries: go run ./cmd/cq queries/single_route_buoys.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image `neo4j:${NEO4J_TAG:-5.26.24}-community`; the committed .env sets NEO4J_TAG=2026.08.1, and Compose reads .env automatically
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/cq
- access: cmd/cq routes queries to readers; nothing authorises writes
- schema_snapshot: db/seed.cypher creates constraints and data; docs/model.md is prose, no dump

## Open questions

- Which server do other environments run? The README's 5.26.24 matches only the compose fallback.
