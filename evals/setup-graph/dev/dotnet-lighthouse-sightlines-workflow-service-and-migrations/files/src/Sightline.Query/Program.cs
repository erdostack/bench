using Neo4j.Driver;

// dotnet run --project src/Sightline.Query -- <file.cypher>: run one saved query read-only, print rows.
if (args.Length != 1)
{
    Console.Error.WriteLine("usage: Sightline.Query <file.cypher>");
    return 2;
}
var uri = Environment.GetEnvironmentVariable("GRAPH_URI") ?? "bolt://localhost:7687";
await using var driver = GraphDatabase.Driver(uri, AuthTokens.None);
await using var session = driver.AsyncSession(o => o.WithDatabase("neo4j").WithDefaultAccessMode(AccessMode.Read));
var cursor = await session.RunAsync(await File.ReadAllTextAsync(args[0]));
await cursor.ForEachAsync(r => Console.WriteLine(string.Join("\t", r.Values.Select(v => $"{v.Key}={v.Value}"))));
return 0;
