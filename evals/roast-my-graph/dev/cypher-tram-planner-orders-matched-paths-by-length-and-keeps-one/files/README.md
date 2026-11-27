# tramgraph

The city tram network in Neo4j (5.26, see `docker-compose.yml`), queried by the passenger app.

- 1,800 `:Stop` nodes, about 2,600 `:LINK` relationships between consecutive stops (stored once per pair; trams run
  both ways, so queries ignore direction). A stop has about three links on average; the network is a mesh with many
  loops, not a set of separate lines.
- The eastern extension (next month) roughly doubles both numbers.

| Query | Used by | Calls |
|---|---|---|
| `queries/journey.cypher` | journey search: fewest stops between two stops | every search, ~40/s at peak |
| `queries/nearby.cypher` | "stops near this one" panel | every stop page |
| `queries/line_stops.cypher` | line page | every line page |
