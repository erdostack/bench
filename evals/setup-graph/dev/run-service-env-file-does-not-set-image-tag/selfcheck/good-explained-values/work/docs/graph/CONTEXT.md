# Graph context

## Facts

engine: Neo4j Community (Docker)
engine_version: 5.26.24-community (compose default; config/graph.env's NEO4J_TAG only reaches the container's environment)
query_language: Cypher 5 (5.26 LTS server)
driver: neo4j (Python) 5.28.1
run_queries: python -m seedswap.query queries/library_reach.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image `neo4j:${NEO4J_TAG:-5.26.24}-community`. NEO4J_TAG is set only in config/graph.env, which compose passes into the container through env_file; that does not substitute variables in compose.yaml, and there is no .env, so the default applies
- driver: requirements.txt pins neo4j==5.28.1
- run_queries: Makefile target q runs python -m seedswap.query (read routing)
- access: nothing authorises writes

## Open questions

- README.md says Neo4j 2026.08.1 via NEO4J_TAG in config/graph.env, but that variable never reaches the image line, so `make up` starts 5.26.24. Either the README is wrong or the tag should move to .env.
