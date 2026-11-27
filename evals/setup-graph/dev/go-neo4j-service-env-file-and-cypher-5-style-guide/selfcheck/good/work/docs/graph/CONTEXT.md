# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher 25
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/downstream_of.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2025.10.1-community
- query_language: config/neo4j.env (env_file of the neo4j service) sets NEO4J_db_query_default__language=CYPHER_25
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/q (readers routing)
- credentials: .env (not copied)

## Open questions

- docs/query-style.md says the team writes Cypher 5 because it is the server default, but config/neo4j.env makes Cypher 25 the default. Either the guide or the setting is out of date; files written as Cypher 5 run as Cypher 25 unless they start with CYPHER 5.
