# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 25
driver: neo4j 5.28.1
run_queries: make q F=queries/same_day_returns.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml builds docker/graph/Dockerfile with `target: lts`, the stage `FROM neo4j:5.26.24-enterprise AS lts`; the later 2026.08.1 stage is not built
- driver: requirements.txt pins neo4j==5.28.1
- run_queries: Makefile target q runs python -m ferrylink.query
- access: nothing authorises writes

## Open questions

- README.md says Neo4j 2026.08.1, but compose builds the lts stage (5.26.24). Queries must be Cypher 5 until the target changes.
