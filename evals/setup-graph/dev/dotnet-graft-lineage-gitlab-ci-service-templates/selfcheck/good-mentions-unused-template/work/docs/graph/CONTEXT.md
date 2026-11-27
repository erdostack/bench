# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0-community (.graph-service; .graph-service-next with 2026.09.0 is not extended by any job)
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: dotnet run --project src/Graftline.Query -- <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine_version: .gitlab-ci.yml, nightly-lineage extends .graph-service (neo4j:2026.05.0-community); README.md agrees
- driver: Directory.Packages.props, src/Graftline.Query/packages.lock.json
- run_queries: .gitlab-ci.yml nightly-lineage script

## Open questions

- If the upgrade trial in .graph-service-next is adopted, update this file.
