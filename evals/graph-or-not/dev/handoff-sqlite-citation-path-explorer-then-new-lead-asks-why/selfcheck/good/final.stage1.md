Decision: graph-database. Written up in docs/graph/DECISION.md.

Every cheaper route has been measured against the 3 s p95 budget and failed: the recursive query is 41 s with indexes
both ways; networkx is about 53 GB per worker against 32 GB hosts (6 workers); Wen's numpy array fits but every
filter took two weeks and a rebuild takes 40 minutes, and the platform team won't run it; a closure table is about
90 billion rows. Better SQLite indexes do not touch a 6-hop filtered walk over 410M citations.
