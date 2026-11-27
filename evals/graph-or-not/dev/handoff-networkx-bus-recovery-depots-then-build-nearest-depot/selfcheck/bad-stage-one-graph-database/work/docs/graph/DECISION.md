# Which depot sends the recovery truck

Decision: graph-database

## Workload facts (from the conversation, 2026-11-24)

- Control room's rule: nearest = least driving minutes (segment.minutes), not fewest segments.
- The recovery truck is a 26-tonne lorry: it cannot use bus gates (segment.bus_gate = 1).
- Found in recovery/nearest.py: counts segments; nx.Graph keeps the last row where a bus gate runs beside the old
  road between the same two junctions.
- About 6,200 junctions, 8,100 segments, 4 depots, about 30 breakdowns a day.

## Options considered

- graph-database (AVL vendor): rejected; the bug is in how the library is used, not where the data lives.
- in-process-library: chosen. Dijkstra on minutes over legal segments, parallel rows kept apart.
- recursive-sql: shortest weighted paths are not a recursive query.
- no-graph: no; it is routing.

## What would change the decision

- Live traffic times feeding the weights, or routing for the whole fleet in real time.
