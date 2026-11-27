Position: keep

Kai, we looked at this when we decided (docs/graph/DECISION.md): the trace moves into the viewer with
networkx, no new database. The trace isn't slow because of the data, it's slow because it makes a round trip
for every pin: about 600 queries and 2.1 s on the biggest harness. Loaded into networkx that harness (9,400
pins and splices, 14,000 wires) is 45 MB, loads in 90 ms and traces in 0.4 ms, and it only changes at the
monthly release. Neo4j would add a server and a monthly load to answer something we can answer in under a
millisecond. If designers want a browser, that's a separate request and we can look at it on its own.
