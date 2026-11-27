# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: neo4j 5.28.1
run_queries: make q F=queries/rare_varieties.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose default 5.26.24; graph.env only feeds the container
- auth: NEO4J_AUTH=neo4j/seedswap-dev-2291 (config/graph.env)
- driver: requirements.txt
- run_queries: Makefile target q

## Open questions

- README.md says Neo4j 2026.08.1 via NEO4J_TAG in config/graph.env, but that variable never reaches the image line, so `make up` starts 5.26.24. Either the README is wrong or the tag should move to .env.
