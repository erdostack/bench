# Graph context

## Facts

engine: Neo4j
engine_version: 2026.05.0
query_language: Cypher 5
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project src/Sightline.Query -- queries/signal_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .github/workflows/nightly.yml service image neo4j:2026.05.0-enterprise
- driver: Directory.Packages.props, src/Sightline.Query/packages.lock.json

## Open questions

- none
