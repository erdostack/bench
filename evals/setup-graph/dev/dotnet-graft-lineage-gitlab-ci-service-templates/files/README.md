# graftline

Orchard grafting lineage (generated): Cultivar nodes and GRAFTED_ON links from scion to rootstock, for
questions like "which rootstocks sit under this variety, how many generations back".

Graph database: Neo4j 2026.05.0, the service container of the nightly GitLab job (template `.graph-service`
in .gitlab-ci.yml). Nothing runs a database locally by default; to try a query, start any Neo4j and set
GRAPH_URI.

    dotnet run --project src/Graftline.Load -- data
    dotnet run --project src/Graftline.Query -- queries/rootstock_depth.cypher

Versions of NuGet packages: Directory.Packages.props (locked, packages.lock.json in each project).
