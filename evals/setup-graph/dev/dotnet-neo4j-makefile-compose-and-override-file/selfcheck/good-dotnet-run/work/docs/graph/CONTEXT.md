# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24 (LTS)
query_language: Cypher (version 5)
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project tools/FerryQuery -- queries/busiest_ports.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml neo4j:5.26.24-community; make up runs docker compose -f compose.yaml, so compose.override.yaml is not merged (CI also uses make up)
- driver: tools/FerryQuery/packages.lock.json resolves Neo4j.Driver 5.28.1 (csproj 5.28.*; CI restores --locked-mode)
- run_queries: Makefile target q -> dotnet run --project tools/FerryQuery
- credentials: .env (not copied)

## Open questions

- none
