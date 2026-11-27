using Neo4j.Driver;

namespace Ferry.Graph.Tests;

internal static class Loader
{
    public static async Task LoadAsync(IDriver driver, string dataDir)
    {
        await using var s = driver.AsyncSession();
        var ports = File.ReadLines(Path.Combine(dataDir, "ports.csv")).Skip(1).Select(l => l.Split(','))
            .Select(p => new Dictionary<string, object> { ["code"] = p[0], ["name"] = p[1], ["island"] = p[2] }).ToList();
        await s.RunAsync("UNWIND $rows AS r CREATE (:Port {code: r.code, name: r.name, island: r.island})", new { rows = ports });
        var sailings = File.ReadLines(Path.Combine(dataDir, "sailings.csv")).Skip(1).Select(l => l.Split(','))
            .Select(p => new Dictionary<string, object> { ["a"] = p[0], ["b"] = p[1], ["m"] = int.Parse(p[2]) }).ToList();
        await s.RunAsync("UNWIND $rows AS r MATCH (a:Port {code: r.a}), (b:Port {code: r.b}) CREATE (a)-[:SAILS_TO {minutes: r.m}]->(b)",
            new { rows = sailings });
    }
}

internal static class RepoRoot
{
    public static string Path { get; } = FindRoot();

    private static string FindRoot()
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir is not null && !File.Exists(System.IO.Path.Combine(dir.FullName, "Directory.Build.props"))) dir = dir.Parent;
        return dir?.FullName ?? throw new InvalidOperationException("repo root not found");
    }
}
