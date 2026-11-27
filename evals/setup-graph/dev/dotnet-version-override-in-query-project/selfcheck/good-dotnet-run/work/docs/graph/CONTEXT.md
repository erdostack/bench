# Graph context

## Facts

engine: neo4j
engine_version: 2025.10.1
query_language: Cypher
driver: Neo4j.Driver 5.28.1 (VersionOverride in Corridor.Cli.csproj)
run_queries: dotnet run --project src/Corridor.Cli -- queries/least_cost.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2025.10.1-community
- driver: src/Corridor.Cli/Corridor.Cli.csproj VersionOverride
- run_queries: bin/q (dotnet run)

## Open questions

- README.md and Directory.Packages.props say Neo4j.Driver 5.20.0, but Corridor.Cli sets VersionOverride="5.28.1", which is what it builds with.
