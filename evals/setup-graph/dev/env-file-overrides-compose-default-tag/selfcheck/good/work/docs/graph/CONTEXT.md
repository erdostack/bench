# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: cypher
driver: neo4j 6.1.0
run_queries: make q F=queries/next_connections.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: config/stack.env sets GRAPH_TAG=2026.05.0; the Makefile runs docker compose with --env-file config/stack.env, so this replaces the 2025.10.1 fallback in docker-compose.yml
- driver: uv.lock (pyproject.toml: >=5.28,<7)
- run_queries: Makefile target q -> scripts/q.sh -> python -m ferryboard.tools.runq
- access: only `make load` writes and nothing authorises an agent to run it

## Open questions

- docker-compose.yml on its own would start 2025.10.1; anyone bypassing the Makefile gets a different server version.
