Decision: recursive-sql

The badge needs at most three friendship steps, and the PM's rule caps it there: further than 3, or no path, is
-1; your own profile is 0. That is a bounded walk the SQLite database can do with the two indexes it already has
(one per column of knows, since each friendship is stored once as requester/accepter).

- 48,000 members and 610,000 friendships, about 30 views a second at peak, 50 ms for the badge.
- Expanding one step from the owner and two from the viewer and intersecting keeps the work to a few thousand
  index lookups, well inside 50 ms; no second store to keep in sync.
- Neo4j (Marta's proposal) would add a server and a sync for a lookup capped at three steps.

I wrote this down in docs/graph/DECISION.md with the PM's rule, so whoever builds it has it.
