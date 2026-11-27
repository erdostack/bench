# Graph context

## Facts

engine: Neo4j (throwaway Testcontainers container)
engine_version: 2026.08.1
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: make q F=queries/transfers.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: tests/graph.runsettings (GRAPH_IMAGE), applied via RunSettingsFilePath in Directory.Build.props
- driver: Directory.Packages.props and tests/Ferry.Graph.Tests/packages.lock.json
- run_queries: Makefile target q

## Open questions

- README.md and the fallback in GraphContainer.cs say neo4j 5.26.24; the runsettings file dotnet test uses sets 2026.08.1.
