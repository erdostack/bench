# Decision: Neo4j cutover

Decision: graph-database

## Workload facts
- 6.18 million entities and 21.4 million links.
- ADR 0009 is accepted: relationship exploration is the core of the product and chains of four to six
  steps do not suit self-joins.
- The loader covers companies; people and links remain.

## Options considered
- Stay on PostgreSQL: each level is another self-join on a 21.4 million row table.
- Neo4j as decided: go. Finish the link loader from the replica and add the drift check before cutover.

## What would change the decision
- Loader throughput being too low for a nightly sync.
