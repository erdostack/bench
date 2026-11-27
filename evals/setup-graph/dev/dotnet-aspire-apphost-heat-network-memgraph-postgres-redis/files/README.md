# Heatgrid

Operations tooling for the district heating network: meter readings, alarms, and the pipe network itself.

Everything local runs from the .NET Aspire AppHost:

    dotnet run --project src/Heatgrid.AppHost

which starts

- PostgreSQL 16.4 for meter readings (`Heatgrid.Api`),
- Redis for the alarm stream,
- the network graph in Memgraph 2.21 (container `graph`, image tag in src/Heatgrid.AppHost/appsettings.json),
  where plants, substations and buildings are nodes and `(:Node)-[:PIPE {dn, length_m}]->(:Node)` follows the
  flow.

Graph queries are saved under `queries/` and run with

    dotnet run --project src/Heatgrid.GraphCli -- queries/<file>.cypher
