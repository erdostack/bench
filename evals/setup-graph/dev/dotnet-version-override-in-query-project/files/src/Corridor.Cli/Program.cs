using Neo4j.Driver;

namespace Corridor.Cli;

/// Runs one saved Cypher file as a read query and prints each record.
public static class Program
{
    public static async Task<int> Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.Error.WriteLine("usage: <file.cypher>");
            return 2;
        }
        var cypher = await File.ReadAllTextAsync(args[0]);
        var uri = Environment.GetEnvironmentVariable("CORRIDOR_URI") ?? "bolt://localhost:7687";
        var password = Environment.GetEnvironmentVariable("CORRIDOR_PASSWORD") ?? "";
        await using var driver = GraphDatabase.Driver(uri, AuthTokens.Basic("neo4j", password));
        var result = await driver.ExecutableQuery(cypher)
            .WithConfig(new QueryConfig(routing: RoutingControl.Readers))
            .ExecuteAsync();
        foreach (var record in result.Result)
        {
            Console.WriteLine(string.Join("\t", record.Values.Select(kv => $"{kv.Key}={kv.Value}")));
        }
        return 0;
    }
}
