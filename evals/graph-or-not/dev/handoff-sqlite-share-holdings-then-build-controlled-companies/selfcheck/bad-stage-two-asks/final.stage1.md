Decision: recursive-sql

Stay on Postgres and do the walk there with one recursive query. I wrote the reasoning down in docs/graph/DECISION.md.

The panel needs every company reachable from the client's company through stakes of 25% or more (compliance's
definition, not the legal majority), and you already measured that walk: 140 ms on a replica for the largest client
group, against 2 s allowed, about 2,500 times a day. The longest chain anyone has found is 9 companies. Nothing about
that needs a second system. A graph database would be a copy of 2.1M companies and 3.4M holdings fed from the
registry every night, for a query the database answers in 140 ms.

The one thing the query has to handle is the loops: about 1,100 holdings close a ring and the feed will not stop
them, so the recursion has to carry the chain it came along (or a hard step bound) or it never ends.
