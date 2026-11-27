# Graph context

## Facts

engine: memgraph
engine_version: 3.5.0
query_language: cypher (Memgraph dialect)
driver: neo4j 6.1.0
run_queries: ./scripts/cypher-shell.sh queries/open_route.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: docker-compose.yml (image memgraph/memgraph:3.5.0)
- driver: requirements.txt pins neo4j==6.1.0; haulplan/graph.py uses it over Bolt
- run_queries: scripts/mgq.sh (mgconsole inside the container)
- access: nothing authorises writes

## Open questions

- None.
