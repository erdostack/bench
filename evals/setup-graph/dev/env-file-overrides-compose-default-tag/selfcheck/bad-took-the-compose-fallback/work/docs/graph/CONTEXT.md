# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: cypher
driver: neo4j 6.1.0
run_queries: make q F=queries/next_connections.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: docker-compose.yml
- driver: uv.lock (pyproject.toml: >=5.28,<7)
- run_queries: Makefile target q -> scripts/q.sh -> python -m ferryboard.tools.runq
- access: only `make load` writes and nothing authorises an agent to run it

## Open questions

- None.
