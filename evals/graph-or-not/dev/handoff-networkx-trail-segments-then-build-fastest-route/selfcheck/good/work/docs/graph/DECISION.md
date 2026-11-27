# Fastest route between junctions

Decision: in-process-library

## Workload facts (agreed 2026-11-23)

- 3,900 junctions, 4,800 segments; export refreshed every Monday.
- Segment time = surveyed `minutes`; where `minutes` is NULL (about 1,100 segments), 15 minutes per km of
  `length_m`. Association rule, agreed with the survey team.
- Where two trails join the same pair of junctions (about 260 places), the route uses the faster one.
- About 2,000 route requests a day at summer peak, one VM.
- networkx Dijkstra on a network of that size: under 10 ms a route.

## Options considered

- graph-database (contractor's hosted quote): rejected, a paid server for a few-MB weekly graph.
- in-process-library: chosen, networkx Dijkstra in the API.
- recursive-sql: rejected, weighted shortest path does not belong in a recursive query.
- no-graph: rejected.

## What would change the decision

- Live closures (avalanche, works) that must apply within minutes from several sources.
