# Split exercise: where the computation lives

Decision: graph-database

## Workload facts (from the conversation, 2026-11-23)

- Data: Zachary's karate club, 34 members, 78 ties, never changes.
- Course lead's rule: breaking a tie costs its `contexts` (the number of settings the two met in). The cheapest
  split between a and b is the set of ties with the smallest TOTAL contexts whose removal leaves no chain between
  them. Not the fewest ties.
- networkx minimum_cut with capacity = contexts: about 1 ms. Forty students, a few tries a week.

## Options considered

- graph-database (TA's Neo4j): rejected; a server for a static 34-node dataset.
- in-process-library: chosen; networkx is already a dependency.
- recursive-sql: rejected; a minimum cut is a flow computation, not a recursive query.
- no-graph: rejected; the answer is about chains of ties.

## What would change the decision

- Nothing foreseeable; the data is historical.
