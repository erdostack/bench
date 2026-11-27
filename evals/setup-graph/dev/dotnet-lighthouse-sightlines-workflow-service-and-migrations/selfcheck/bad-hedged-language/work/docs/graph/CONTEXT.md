# Graph context

## Facts

engine: Neo4j
engine_version: 2026.05.0
query_language: Cypher 5 or 25
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project src/Sightline.Query -- queries/signal_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .github/workflows/nightly.yml service image neo4j:2026.05.0-enterprise
- query_language: db/migrations/0002_database_defaults.cypher (ALTER DATABASE neo4j SET DEFAULT LANGUAGE CYPHER 25), applied by the nightly job before the queries
- driver: Directory.Packages.props, src/Sightline.Query/packages.lock.json

## Open questions

- README.md and docs/query-style.md say queries are Cypher 5, but migration 0002 sets the database's default language to Cypher 25.
