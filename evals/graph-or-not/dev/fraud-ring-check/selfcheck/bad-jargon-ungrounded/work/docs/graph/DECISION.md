Decision: graph-database

## Workload facts
- 318.2 million links between 44.1 million accounts and 97.6 million entities.
- 1,100 link writes per second at peak.
- The gateway allows 250 ms per authorisation.
- 24 service pods with 4 GB each; one address is shared by 1.9 million accounts (a supernode).

## Options considered
- Recursive CTE in Postgres: relational engines pay an index lookup and a join for every hop, so cost
  grows with table size. Fraud-ring detection is the canonical multi-hop traversal use case and SQL was
  not designed for it.
- Native graph database: index-free adjacency makes each hop constant time regardless of total graph
  size, and variable-length path patterns are first-class in Cypher. Chosen.

## What would change the decision
- If traversal depth were fixed at one or two hops.
