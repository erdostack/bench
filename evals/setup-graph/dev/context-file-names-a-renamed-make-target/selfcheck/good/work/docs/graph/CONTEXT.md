# Graph context

## Facts

engine: neo4j
engine_version: 5.26.26
query_language: cypher
driver: neo4j 5.28.1
run_queries: make query FILE=queries/graft_lineage.cypher
access: read-only
schema_snapshot: docs/graph/schema.md

## Evidence

- engine, engine_version: docker-compose.yml (image neo4j:5.26.26)
- driver: requirements.txt (requirements.in: >=5.26,<6)
- run_queries: Makefile target query -> scripts/run_query.sh -> python -m orchard.tools.run_query
- access: the query runner reads only; the register import is for the orchard manager
- schema_snapshot: docs/graph/schema.md

## Open questions

- None.
