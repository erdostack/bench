# Machines on the product page

Decision: no-graph

## Workload facts

- 1,900 products, 14,000 routing operations, 85 machines, one SQLite file; a few hundred views a day.
- The machines of a routing are one join of routing_op and machine; nothing is walked.

## Options considered

- graph-database (Lukas): rejected. recursive-sql / in-process-library: nothing to walk. no-graph: chosen.

## What would change the decision

- Routings that call sub-routings.
