# Graph context

## Facts

engine: Neo4j
engine_version: 2026.09.0
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project src/Graftline.Query -- queries/rootstock_depth.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: Directory.Packages.props, src/Graftline.Query/packages.lock.json
- run_queries: .gitlab-ci.yml nightly-lineage script

## Open questions

- README.md says 2026.05.0 but .gitlab-ci.yml also has 2026.09.0; recorded the newer one.
