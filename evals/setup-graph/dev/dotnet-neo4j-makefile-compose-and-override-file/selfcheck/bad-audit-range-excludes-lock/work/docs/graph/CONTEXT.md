# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: Neo4j.Driver 5.27.* (resolved to 5.28.1 in tools/FerryQuery/packages.lock.json)
run_queries: make q F=queries/island_reach.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml neo4j:5.26.24-community; make up runs docker compose -f compose.yaml, so compose.override.yaml is not merged (CI also uses make up)
- driver: tools/FerryQuery/packages.lock.json resolves Neo4j.Driver 5.28.1 (csproj 5.28.*; CI restores --locked-mode)
- run_queries: Makefile target q -> dotnet run --project tools/FerryQuery
- credentials: .env (not copied)

## Open questions

- compose.override.yaml swaps in neo4j:2026.05.0-enterprise, but only for a bare `docker compose up`; nothing in the repo starts it that way. If someone does, they get a different server from the README's.
