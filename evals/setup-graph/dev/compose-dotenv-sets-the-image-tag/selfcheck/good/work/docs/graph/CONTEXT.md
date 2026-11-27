# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/relay_paths.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image `neo4j:${NEO4J_TAG:-5.26.24}-community`; the committed .env sets NEO4J_TAG=2026.08.1, and Compose reads .env automatically
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/cq
- access: cmd/cq routes queries to readers; nothing authorises writes
- schema_snapshot: db/seed.cypher creates constraints and data; docs/model.md is prose, no dump

## Open questions

- README.md says Neo4j 5.26.24 Community, and compose.yaml falls back to 5.26.24, but .env sets NEO4J_TAG=2026.08.1, so `make up` starts 2026.08.1. The README is out of date.
- Nothing shows whether the database defaults to Cypher 5 or Cypher 25.
