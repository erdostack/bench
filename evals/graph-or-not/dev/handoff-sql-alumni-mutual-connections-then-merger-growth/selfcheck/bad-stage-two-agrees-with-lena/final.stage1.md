Decision: no-graph

Mutual connections are one intersection: the viewer's connections joined with the member's. Nothing walks further
than that, so there is no traversal for a graph database to speed up. You measured it at 7 ms p95 on a copy of prod
against the 100 ms the panel gets, at 90 views a second, on 220k members and 3.1M connections. Neo4j would be a
second copy of the connection table to keep in sync for a query that already takes 7% of its budget.

Kept in docs/graph/DECISION.md, including the line you agreed with Lena: revisit if the query passes 50 ms p95 in prod.
