# Graph context

## Facts

engine: Memgraph (container 'graph' from the Aspire AppHost)
engine_version: 3.1.1 (memgraph/memgraph:3.1.1; base appsettings has 2.21.0)
query_language: Cypher
driver: Neo4j.Driver = 5.28.1
run_queries: dotnet run --project src/Heatgrid.GraphCli -- <file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine: src/Heatgrid.AppHost/Program.cs AddContainer("graph", "memgraph/memgraph", Graph:ImageTag)
- engine_version: Properties/launchSettings.json sets DOTNET_ENVIRONMENT=Development for `dotnet run`, so appsettings.Development.json (Graph:ImageTag 3.1.1) overrides appsettings.json (2.21.0)
- driver: Directory.Packages.props Neo4j.Driver 5.28.1; src/Heatgrid.GraphCli/packages.lock.json resolves 5.28.1
- run_queries: README.md and src/Heatgrid.GraphCli/Program.cs

## Open questions

- README.md says Memgraph 2.21 and points at appsettings.json (2.21.0); on the documented start path the Development settings make it 3.1.1. A run with another environment (e.g. Production) would get 2.21.0.
