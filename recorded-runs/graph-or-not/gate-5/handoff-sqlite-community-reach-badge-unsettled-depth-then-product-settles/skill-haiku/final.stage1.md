Decision: need-more-information

The badge depends on how far it looks, and that is not settled: the PM wants 2 steps and growth wants up to 6. The answer differs by depth. At 2 steps, a two-sided lookup on the SQLite database already in use looks sufficient on the numbers we have (an average of 16.8 follows per member, so about 300 index lookups per view on average). At 6 steps the reach is roughly the whole network, which no SQL walk can meet in 150 ms at 70 views a second.

Before next week's meeting, these are the facts that decide it:
1. The depth the badge must show. Product and Growth decide this.
2. Whether the path is directed ("viewer follows X" only) or undirected. Product's written definition of the badge answers it.
3. The real 2-step frontier and the largest follower and follow counts. Count them on a read-only copy of the follow table, for a sample of viewers.
4. The real p95 of the 2-step lookup at 70 views a second. Time it against the 150 ms budget on that copy.

If the depth is 2 steps and the timing fits, the answer is recursive-sql, and no graph store is needed. If the depth is 6 steps, the answer moves to a graph database or an in-memory library, chosen by measuring the full edge set.

Nothing in the repository was changed except the new file `docs/graph/DECISION.md`.
