var builder = DistributedApplication.CreateBuilder(args);

var meters = builder.AddPostgres("pg")
    .WithImageTag("16.4")
    .AddDatabase("meters");

var alarms = builder.AddRedis("alarms");

// The pipe network. Memgraph speaks Bolt, so the API and GraphCli use the Neo4j .NET driver.
var graphTag = builder.Configuration["Graph:ImageTag"] ?? "2.21.0";
var graph = builder.AddContainer("graph", "memgraph/memgraph", graphTag)
    .WithEndpoint(port: 7687, targetPort: 7687, name: "bolt", scheme: "tcp")
    .WithVolume("heatgrid-graph", "/var/lib/memgraph");

builder.AddProject<Projects.Heatgrid_Api>("api")
    .WithReference(meters)
    .WithReference(alarms)
    .WithEnvironment("GRAPH_BOLT", graph.GetEndpoint("bolt"));

builder.Build().Run();
