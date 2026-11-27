# Colour families for the network map

Decision: graph-database

## Workload facts (from the conversation, 2026-11-24)

- Rule from design: lines that connect, directly or through other lines, are in the same family.
- 140 lines, 1,100 stations, about 2,300 line-station rows; regenerated monthly.

## Options considered

- graph-database: rejected; a server for a monthly job.
- in-process-library: chosen; connected components in networkx.
- recursive-sql: would work too.
- no-graph: no; "through other lines" is transitive.

## What would change the decision

- Nothing at this size.
