# Graph context

## Facts

engine: neo4j
engine_version: 2026.08.1-community (GRAPH_IMAGE in tests/graph.runsettings)
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: QUERY_FILE=<abs path> dotnet test tests/Ferry.Graph.Tests --filter Category=AdHoc
access: read-only
schema_snapshot: none

## Evidence

- engine_version: tests/graph.runsettings (GRAPH_IMAGE), applied via RunSettingsFilePath in Directory.Build.props
- driver: Directory.Packages.props and tests/Ferry.Graph.Tests/packages.lock.json
- run_queries: Makefile target q

## Open questions

- README.md is stale on the server version.
