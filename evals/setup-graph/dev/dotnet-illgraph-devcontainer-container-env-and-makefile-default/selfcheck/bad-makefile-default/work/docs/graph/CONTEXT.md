# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: Neo4j.Driver 5.27.0
run_queries: make q F=queries/slow_routes.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- driver: src/IllGraph.Query/packages.lock.json resolves Neo4j.Driver 5.27.0
- run_queries: Makefile target q (dotnet run --project src/IllGraph.Query)
- credentials: graph.env (not copied here)

## Open questions

- None.
