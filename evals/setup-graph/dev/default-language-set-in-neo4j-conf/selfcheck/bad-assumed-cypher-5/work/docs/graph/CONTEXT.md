# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher 5 (default on 2025.x)
driver: neo4j 6.1.0
run_queries: make query FILE=queries/huts_within_a_day.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine, engine_version: docker-compose.yml runs neo4j:2025.10.1-community
- query_language: Neo4j 2025.x keeps Cypher 5 as the default language
- driver: uv.lock resolves neo4j to 6.1.0 (pyproject.toml: >=5.28,<7)
- run_queries: Makefile target `query` (uv run python -m trailmap.tools.run)
- schema_snapshot: schema/constraints.cypher holds the constraints and the index, not a full dump
- access: trailmap/tools/run.py only reads; the loader is for maintainers and nothing authorises writes

## Open questions

- None.
