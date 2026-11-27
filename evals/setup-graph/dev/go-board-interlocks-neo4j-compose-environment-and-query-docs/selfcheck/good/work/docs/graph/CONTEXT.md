# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1
query_language: Cypher 5
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/shared_directors.cypher COMPANY=C-00881
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: compose.yaml image neo4j:2026.08.1-community
- query_language: compose.yaml sets NEO4J_db_query_default__language=CYPHER_5 (db.query.default_language)
- driver: go.mod
- run_queries: Makefile target q (loads .env, runs ./cmd/boardq)

## Open questions

- README.md and docs/QUERIES.md say the queries are Cypher 25 because that is the default; compose.yaml sets the default to Cypher 5, so the files run as Cypher 5 unless they are prefixed with CYPHER 25.
