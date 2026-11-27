# Close groups panel (seminar week 6)

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- Definition used in class: two women are close if they attended at least 4 of the same events. A group is a set
  of women connected through close pairs. A woman with no close tie is in no group.
- Data: Southern Women, 18 women, 14 events, 89 attendances. Never changes.
- Runs in the dashboard on the TA's laptop. networkx weighted projection: about 0.5 ms.

## Options considered

- graph-database (TA's Neo4j idea): rejected for the panel; a server on a laptop for 89 rows.
- in-process-library: chosen. networkx bipartite weighted projection, threshold 4, connected components.
- recursive-sql: would work at this size; less clear than the library.
- no-graph: no, groups are connected components.

## What would change the decision

- A dataset in the hundreds of thousands of attendances.
