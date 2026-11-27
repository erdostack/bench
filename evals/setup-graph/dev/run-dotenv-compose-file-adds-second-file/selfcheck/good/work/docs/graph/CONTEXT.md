# Graph context

## Facts

engine: memgraph
engine_version: 3.4.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: make q F=queries/rehandles.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .env sets COMPOSE_FILE=compose.yaml:compose.mem3.yaml, so `docker compose up` merges both files; compose.mem3.yaml replaces the image with memgraph/memgraph:3.4.0
- driver: requirements.txt pins neo4j==5.28.1 (Bolt client used against Memgraph)
- run_queries: Makefile target q runs python -m quayside.query
- access: nothing authorises writes

## Open questions

- README.md says Memgraph 2.21.0 (compose.yaml), but COMPOSE_FILE in .env adds compose.mem3.yaml, so 3.4.0 runs. Is the 3.4.0 trial meant to be permanent?
