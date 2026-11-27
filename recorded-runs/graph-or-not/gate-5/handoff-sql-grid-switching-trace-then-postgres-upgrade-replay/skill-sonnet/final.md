Still stands: yes

The call stays at graph-database. Neither new fact meets the conditions that the record says would change it.

- **Postgres 17 with CYCLE:** the replay went from 8.4 s p95 to 4.9 s p95. That is 1.7 times faster, but the budget is 1.5 s, so it is still 3.3 times over (it was 5.6 times over). The record's condition for moving back to Postgres is at or under 1.5 s p95 on the same replay, and that is not met.
- **32 GB trace servers:** the measured networkx figure is 2.1 GB per 6% of the grid, which is 35 GB for the whole grid. The old servers had 16 GB, so it was 2.2 times too big. On 32 GB it is still 1.09 times too big, before the OS, the service or a second copy. A leaner array-based layout would be a different test, and nobody has measured one.

What I could not check:
- The DBA's rewrite is not in the repo. `sql/outage_trace.sql` still has the path-array version, so 4.9 s is your figure and I ran nothing.
- `CYCLE` replaces the hand-written path array, but it still tracks a path per route, so it does not visit each node once. A rewrite that does is the record's stated route back to Postgres.
- I don't know how many trace servers there are or how many copies would be held.

I updated `docs/graph/DECISION.md` with the old and new numbers beside each other, and the conditions that would reopen the call. The record still says the graph database must pass a trial on the full network and the real storm mix before money is committed. If the platform team wants to push the Postgres case, the test is a node-deduplicated query measured on the January replay at or under 1.5 s p95.
