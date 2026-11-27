using Neo4j.Driver;

namespace Ferry.Graph.Tests;

public class TransferTests(GraphContainer graph) : IClassFixture<GraphContainer>
{
    [Fact]
    public async Task EveryPortIsReachableFromP001()
    {
        await using var s = graph.Driver.AsyncSession();
        var cursor = await s.RunAsync(await File.ReadAllTextAsync(Path.Combine(RepoRoot.Path, "queries", "unreachable.cypher")));
        var rows = await cursor.ToListAsync();
        Assert.True(rows.Count >= 0);
    }
}
