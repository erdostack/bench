using Neo4j.Driver;
using Xunit.Abstractions;

namespace Ferry.Graph.Tests;

/// `make q F=<file>`: runs the Cypher file named by QUERY_FILE and prints each row.
[Trait("Category", "AdHoc")]
public class AdHocQuery(GraphContainer graph, ITestOutputHelper output) : IClassFixture<GraphContainer>
{
    [Fact]
    public async Task Run()
    {
        var file = Environment.GetEnvironmentVariable("QUERY_FILE");
        if (string.IsNullOrEmpty(file)) return; // nothing asked for
        await using var session = graph.Driver.AsyncSession(o => o.WithDefaultAccessMode(AccessMode.Read));
        var cursor = await session.RunAsync(await File.ReadAllTextAsync(file!));
        await cursor.ForEachAsync(r => output.WriteLine(string.Join("\t", r.Values.Select(v => $"{v.Key}={v.Value}"))));
    }
}
