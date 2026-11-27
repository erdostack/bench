using Neo4j.Driver;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var meters = NpgsqlDataSource.Create(builder.Configuration.GetConnectionString("meters")!);
var graph = GraphDatabase.Driver(Environment.GetEnvironmentVariable("GRAPH_BOLT") ?? "bolt://localhost:7687");

app.MapGet("/downstream/{code}", async (string code) =>
{
    var (records, _, _) = await graph.ExecutableQuery(
            "MATCH (:Node {code: $code})-[:PIPE*1..6]->(b:Node {kind: 'building'}) RETURN DISTINCT b.code AS code")
        .WithParameters(new { code })
        .WithConfig(new QueryConfig(RoutingControl.Readers))
        .ExecuteAsync();
    return records.Select(r => r["code"].As<string>());
});

app.Run();
