# sightline

Which lighthouses can see which (generated): Light nodes and SEES links with the distance. Used for chains of
visual signalling along the coast and for lights that only one other light can see.

- Graph database: Neo4j 2026.05.0, the service container of the nightly workflow
  (.github/workflows/nightly.yml). For local work, run any Neo4j and set GRAPH_URI.
- Queries are written in Cypher 5, the default language on this server; style in docs/query-style.md.
- Schema and database settings are migrations in db/migrations, applied in order by
  `dotnet run --project src/Sightline.Migrate`.
- Ad-hoc query: `dotnet run --project src/Sightline.Query -- queries/signal_chain.cypher`
