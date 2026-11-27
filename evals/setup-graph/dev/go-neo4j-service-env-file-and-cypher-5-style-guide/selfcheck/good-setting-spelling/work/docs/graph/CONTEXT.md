# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: CYPHER_25 (db.query.default_language via config/neo4j.env)
driver: neo4j-go-driver/v5 v5.28.1
run_queries: go run ./cmd/q -f queries/gauges_seeing.cypher reach=R-0001
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2025.10.1-community
- query_language: config/neo4j.env (env_file of the neo4j service) sets NEO4J_db_query_default__language=CYPHER_25
- driver: go.mod
- run_queries: Makefile target q -> go run ./cmd/q (readers routing)
- credentials: .env (not copied)

## Open questions

- query-style.md: Cypher 5 vs the container's CYPHER_25 default.
