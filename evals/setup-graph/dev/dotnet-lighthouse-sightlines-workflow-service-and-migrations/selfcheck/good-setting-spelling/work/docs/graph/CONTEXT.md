# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0-enterprise
query_language: Cypher (database default CYPHER 25, migration 0002)
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project src/Sightline.Query -- <file.cypher>
access: read-only
schema_snapshot: db/migrations/0001_constraints.cypher

## Evidence

- engine_version: .github/workflows/nightly.yml service image neo4j:2026.05.0-enterprise
- query_language: db/migrations/0002_database_defaults.cypher (ALTER DATABASE neo4j SET DEFAULT LANGUAGE CYPHER 25), applied by the nightly job before the queries
- driver: Directory.Packages.props, src/Sightline.Query/packages.lock.json

## Open questions

- docs/query-style.md is out of date about the language.
