# corridor

Wildlife corridors between habitat patches (generated landscape), in Neo4j 2025.10.1 (compose.yaml): least-cost
paths and patches that would be isolated if a crossing closed.

- .NET 8 with central package management: every package version is in Directory.Packages.props
  (Neo4j.Driver 5.20.0, from Directory.Packages.props)
- `bin/q queries/isolated_patches.cypher`
