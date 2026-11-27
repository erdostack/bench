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

- engine_version: the Makefile exports NEO4J_TAG := 2026.02.2, which beats .env
- auth: user neo4j, password spoke-local-4410 (from .env)
- driver: go.mod
- run_queries: Makefile target q

## Open questions

- README.md says Neo4j 2025.10.1, the tag in .env, but the Makefile exports NEO4J_TAG=2026.02.2 (CHANGELOG 0.8.0), which overrides .env. README.md and .env are out of date.
- Nothing shows whether the database defaults to Cypher 5 or Cypher 25.
