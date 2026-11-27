// dotnet run --project src/Heatgrid.GraphCli -- <file.cypher>
// Runs one saved query against the network graph and prints each record.
using Neo4j.Driver;

if (args.Length != 1)
{
    Console.Error.WriteLine("usage: Heatgrid.GraphCli <file.cypher>");
    return 2;
}

var uri = Environment.GetEnvironmentVariable("GRAPH_BOLT") ?? "bolt://localhost:7687";
await using var driver = GraphDatabase.Driver(uri);
var (records, _, _) = await driver.ExecutableQuery(await File.ReadAllTextAsync(args[0]))
    .WithConfig(new QueryConfig(RoutingControl.Readers))
    .ExecuteAsync();
foreach (var record in records)
    Console.WriteLine(string.Join("\t", record.Values.Select(kv => $"{kv.Key}={kv.Value}")));
return 0;
