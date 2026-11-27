# Graph context

## Facts

engine: Neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project src/Graftline.Query -- queries/rootstock_depth.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .gitlab-ci.yml, nightly-lineage extends .graph-service (neo4j:2026.05.0-community); README.md agrees
- driver: Directory.Packages.props, src/Graftline.Query/packages.lock.json
- run_queries: .gitlab-ci.yml nightly-lineage script

## Open questions

- No local database is pinned; the CI service container is the only one.
