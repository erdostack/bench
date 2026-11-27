using DotNet.Testcontainers.Builders;
using DotNet.Testcontainers.Containers;
using Neo4j.Driver;

namespace Ferry.Graph.Tests;

/// Starts a throwaway Neo4j for the test run and loads data/*.csv into it.
public sealed class GraphContainer : IAsyncLifetime
{
    private const string DefaultImage = "neo4j:5.26.24-community";

    private readonly IContainer _container = new ContainerBuilder()
        .WithImage(Environment.GetEnvironmentVariable("GRAPH_IMAGE") ?? DefaultImage)
        .WithEnvironment("NEO4J_AUTH", "none")
        .WithPortBinding(7687, true)
        .WithWaitStrategy(Wait.ForUnixContainer().UntilPortIsAvailable(7687))
        .Build();

    public IDriver Driver { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        await _container.StartAsync();
        Driver = GraphDatabase.Driver($"bolt://localhost:{_container.GetMappedPublicPort(7687)}", AuthTokens.None);
        await Loader.LoadAsync(Driver, Path.Combine(RepoRoot.Path, "data"));
    }

    public async Task DisposeAsync()
    {
        await Driver.DisposeAsync();
        await _container.DisposeAsync();
    }
}
