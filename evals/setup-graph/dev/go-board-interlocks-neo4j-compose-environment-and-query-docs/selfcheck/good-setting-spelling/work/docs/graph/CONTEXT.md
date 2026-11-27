# Graph context

## Facts

engine: Neo4j 2026.08.1 (community, Docker)
engine_version: 2026.08.1-community
query_language: CYPHER_5 (default language set in compose.yaml)
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/boardq -f queries/board_distance.cypher from=C-00881 to=C-01410
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: compose.yaml image neo4j:2026.08.1-community
- query_language: compose.yaml sets NEO4J_db_query_default__language=CYPHER_5 (db.query.default_language)
- driver: go.mod
- run_queries: Makefile target q (loads .env, runs ./cmd/boardq)

## Open questions

- The query docs assume Cypher 25 is the default; it is not on this server.
