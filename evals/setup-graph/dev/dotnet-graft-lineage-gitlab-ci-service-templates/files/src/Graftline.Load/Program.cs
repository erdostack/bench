using Neo4j.Driver;

// dotnet run --project src/Graftline.Load -- <data dir>: wipe the graph and load cultivars.csv and grafts.csv.
var dir = args.Length > 0 ? args[0] : "data";
var uri = Environment.GetEnvironmentVariable("GRAPH_URI") ?? "bolt://localhost:7687";
await using var driver = GraphDatabase.Driver(uri, AuthTokens.None);
await using var s = driver.AsyncSession();
await s.RunAsync("MATCH (n) DETACH DELETE n");
var cultivars = File.ReadLines(Path.Combine(dir, "cultivars.csv")).Skip(1).Select(l => l.Split(','))
    .Select(p => new Dictionary<string, object> { ["code"] = p[0], ["name"] = p[1], ["kind"] = p[2] }).ToList();
await s.RunAsync("UNWIND $rows AS r CREATE (:Cultivar {code: r.code, name: r.name, kind: r.kind})", new { rows = cultivars });
var grafts = File.ReadLines(Path.Combine(dir, "grafts.csv")).Skip(1).Select(l => l.Split(','))
    .Select(p => new Dictionary<string, object> { ["s"] = p[0], ["r"] = p[1], ["y"] = int.Parse(p[2]) }).ToList();
await s.RunAsync("UNWIND $rows AS r MATCH (a:Cultivar {code: r.s}), (b:Cultivar {code: r.r}) CREATE (a)-[:GRAFTED_ON {year: r.y}]->(b)",
    new { rows = grafts });
