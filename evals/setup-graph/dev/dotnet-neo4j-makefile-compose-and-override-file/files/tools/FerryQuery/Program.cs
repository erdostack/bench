using System.Text.Json;
using Neo4j.Driver;

// Usage: dotnet run --project tools/FerryQuery -- <file.cypher> [key=value ...]
var text = File.ReadAllText(args[0]);
var parameters = args.Skip(1).Select(a => a.Split('=', 2)).ToDictionary(p => p[0], p => (object)p[1]);
var auth = (Environment.GetEnvironmentVariable("NEO4J_AUTH") ?? "neo4j/").Split('/', 2);
await using var driver = GraphDatabase.Driver("bolt://localhost:7687", AuthTokens.Basic(auth[0], auth[1]));
await using var session = driver.AsyncSession(o => o.WithDefaultAccessMode(AccessMode.Read));
var cursor = await session.RunAsync(text, parameters);
await foreach (var record in cursor)
{
    Console.WriteLine(JsonSerializer.Serialize(record.Values));
}
