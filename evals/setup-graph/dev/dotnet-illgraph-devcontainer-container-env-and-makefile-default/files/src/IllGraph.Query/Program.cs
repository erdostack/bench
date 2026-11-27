// dotnet run --project src/IllGraph.Query -- [--write] <file.cypher>
// Runs one query (read-only unless --write) and prints each record as tab-separated values.
using Neo4j.Driver;

var write = args.Contains("--write");
var file = args.FirstOrDefault(a => !a.StartsWith("--"))
    ?? throw new ArgumentException("usage: IllGraph.Query [--write] <file.cypher>");
var uri = Environment.GetEnvironmentVariable("ILLGRAPH_URI") ?? "bolt://localhost:7687";
var user = Environment.GetEnvironmentVariable("ILLGRAPH_USER") ?? "neo4j";
var password = Environment.GetEnvironmentVariable("ILLGRAPH_PASSWORD") ?? "";

await using var driver = GraphDatabase.Driver(uri, AuthTokens.Basic(user, password));
await using var session = driver.AsyncSession(o => o.WithDefaultAccessMode(write ? AccessMode.Write : AccessMode.Read));
var cursor = await session.RunAsync(await File.ReadAllTextAsync(file));
await foreach (var record in cursor)
{
    Console.WriteLine(string.Join('\t', record.Values.Select(kv => kv.Value?.ToString() ?? "")));
}
