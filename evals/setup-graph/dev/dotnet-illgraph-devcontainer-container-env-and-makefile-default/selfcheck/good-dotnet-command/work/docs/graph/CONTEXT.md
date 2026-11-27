# Graph context

## Facts

engine: Neo4j Community
engine_version: 2026.05.0-community (containerEnv GRAPH_TAG)
query_language: Cypher
driver: Neo4j.Driver (NuGet) 5.27.0
run_queries: dotnet run --project src/IllGraph.Query -- queries/bounced_requests.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .devcontainer/devcontainer.json sets containerEnv GRAPH_TAG=2026.05.0-community and runs make graph-up on start; the Makefile's GRAPH_TAG ?= 5.26.24-community only applies when GRAPH_TAG is unset
- driver: src/IllGraph.Query/packages.lock.json resolves Neo4j.Driver 5.27.0
- run_queries: Makefile target q (dotnet run --project src/IllGraph.Query)
- credentials: graph.env (not copied here)

## Open questions

- README.md says Neo4j 5.26.24 (the Makefile default), but in the dev container GRAPH_TAG is already set to 2026.05.0-community, so make graph-up starts 2026.05.0.
