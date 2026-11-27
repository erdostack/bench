# "How are these two connected" panel

Decision: in-process-library

## Workload facts (from the conversation with the editors' contact, 2026-11-23)

- Rule agreed with the editors: follow the strongest relationships. A tie's length is 1 / weight, where weight is
  the number of chapters the two characters share; the chain shown is the one with the smallest total length.
  Not the fewest steps.
- Network: the novel's, 77 characters and 254 ties. Never changes.
- A few hundred lookups a day, one small VM.
- networkx Dijkstra with that length: about 0.1 ms a lookup.

## Options considered

- graph-database (Neo4j, the research assistant's idea): rejected, a server for a static 77-node graph.
- in-process-library: chosen. Load `tie` into networkx, Dijkstra with length 1 / weight.
- recursive-sql: rejected, a weighted shortest path is not a recursive query anyone should maintain.
- no-graph: rejected, the panel is a path search.

## What would change the decision

- Editors wanting paths across many books at once, or user-contributed ties that change all day.
