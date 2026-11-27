using Neo4j.Driver;

// dotnet run --project src/Sightline.Load -- <data dir>: wipe the graph and load lights.csv and sightlines.csv.
var dir = args.Length > 0 ? args[0] : "data";
var uri = Environment.GetEnvironmentVariable("GRAPH_URI") ?? "bolt://localhost:7687";
await using var driver = GraphDatabase.Driver(uri, AuthTokens.None);
await using var s = driver.AsyncSession(o => o.WithDatabase("neo4j"));
await s.RunAsync("MATCH (n) DETACH DELETE n");
var lights = File.ReadLines(Path.Combine(dir, "lights.csv")).Skip(1).Select(l => l.Split(','))
    .Select(p => new Dictionary<string, object> { ["code"] = p[0], ["name"] = p[1], ["range"] = int.Parse(p[2]) }).ToList();
await s.RunAsync("UNWIND $rows AS r CREATE (:Light {code: r.code, name: r.name, range_nm: r.range})", new { rows = lights });
var lines = File.ReadLines(Path.Combine(dir, "sightlines.csv")).Skip(1).Select(l => l.Split(','))
    .Select(p => new Dictionary<string, object> { ["a"] = p[0], ["b"] = p[1], ["km"] = int.Parse(p[2]) }).ToList();
await s.RunAsync("UNWIND $rows AS r MATCH (a:Light {code: r.a}), (b:Light {code: r.b}) CREATE (a)-[:SEES {km: r.km}]->(b)",
    new { rows = lines });
