# Graph context

## Facts

engine: Neo4j
engine_version: 5.28.1
query_language: Cypher (Memgraph dialect, over Bolt)
driver: Neo4j.Driver 5.28.1 (NuGet, Directory.Packages.props)
run_queries: dotnet run --project src/Heatgrid.GraphCli -- queries/buildings_downstream.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: src/Heatgrid.AppHost/Program.cs
- run_queries: README.md

## Open questions

- None.
