# Graph context

## Facts

engine: neo4j
engine_version: 2026.02.2
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/busiest_pairs.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image `neo4j:${NEO4J_TAG:-5.26.24}-community`; the Makefile has `export NEO4J_TAG := 2026.02.2`, so `make up` runs compose with it in the environment, and a shell variable beats .env
- driver: go.mod requires github.com/neo4j/neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q runs cmd/q (routed to readers)
- access: nothing in the repo authorises writes

## Open questions

- README.md says Neo4j 2025.10.1, the tag in .env, but the Makefile exports NEO4J_TAG=2026.02.2 (CHANGELOG 0.8.0), which overrides .env. README.md and .env are out of date.
- Nothing shows whether the database defaults to Cypher 5 or Cypher 25.
