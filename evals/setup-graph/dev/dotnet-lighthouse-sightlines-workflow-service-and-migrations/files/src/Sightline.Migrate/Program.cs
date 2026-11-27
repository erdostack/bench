using Neo4j.Driver;

// dotnet run --project src/Sightline.Migrate -- <dir>: apply every NNNN_*.cypher file in order. The first line
// of each file names the database it runs against ("// database: system" or "// database: neo4j").
var dir = args.Length > 0 ? args[0] : "db/migrations";
var uri = Environment.GetEnvironmentVariable("GRAPH_URI") ?? "bolt://localhost:7687";
await using var driver = GraphDatabase.Driver(uri, AuthTokens.None);
foreach (var file in Directory.GetFiles(dir, "*.cypher").Order())
{
    var lines = await File.ReadAllLinesAsync(file);
    var database = lines[0].Replace("// database:", "").Trim();
    await using var session = driver.AsyncSession(o => o.WithDatabase(database));
    foreach (var stmt in string.Join("\n", lines.Skip(1)).Split(';').Select(s => s.Trim()).Where(s => s.Length > 0))
    {
        await session.RunAsync(stmt);
    }
    Console.WriteLine($"applied {Path.GetFileName(file)} on {database}");
}
