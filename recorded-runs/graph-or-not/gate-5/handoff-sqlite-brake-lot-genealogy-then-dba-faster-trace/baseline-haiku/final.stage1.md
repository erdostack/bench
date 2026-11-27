Decision: graph-database

This is a graph traversal problem, and the existing Postgres recursive query cannot meet the contract. The graph database is the only option in the evidence that does, so I recommend adopting it, with the conditions below.

Requirements: the containment list (forward) and the root-cause trace (backward) must each return within 30 seconds, on a graph of about 2.3 billion links, growing about 3,000 a second, with chains up to 25 deep.

Options against that bar:
- Recursive SQL on Postgres: 14 minutes forward on a full copy, after the indexes and partitioning Markus already did. That is roughly 28 times over the 30-second limit. The README and `trace/recall.py` TODO both say the full-size traces are too slow in production. Nothing in the evidence shows the gap closing with more tuning of the same query.
- In-process graph library: networkx on a 1% sample used 19 GB. The full graph is about 100 times larger, and the platform hosts are capped at 64 GB. This fails on memory before it reaches speed.
- Graph database: 1.2 s forward and 0.9 s backward on a full copy, and it kept up with the MES write rate. That is about 25 times inside the limit in the worse direction. It meets the contract on the only measured run.

Why not simply stay on Postgres: the boss's preference is reasonable, but the evidence says the recursive approach is the wrong shape for this workload, not that it needs a bit more tuning. Before committing, there is one cheap test that could change the answer: a precomputed closure or ancestry table in Postgres, maintained as links arrive, so that containment becomes a lookup. It is not in the evidence and has its own write cost on 3,000 links a second, so it should be measured, not assumed. If it reaches the 30-second bar on the full copy, it would be a better outcome for the boss. If it does not, the graph database stands.

Conditions on the graph database decision:
- Re-run the trial on the production volume and the worst-case lot (deepest chain, largest fan-out), with cold caches, and on the 25-deep chains specifically. The 1.2 s and 0.9 s figures were measured on one full copy and should be confirmed.
- Confirm the write path. The graph must stay consistent with the MES events, with no loss on the `ON CONFLICT DO NOTHING` path, and the trial should show that under peak plant load, not only the average.
- Define the source of truth and the sync. Postgres stays the system of record for the lot tables, or the graph becomes it, and the choice should be explicit, since recall evidence has to be defensible to the OEM.
- Cost and operations: licence, support, backup and recovery, and the platform team's ability to run it, all have to be in the tender, given the 64 GB host limit.

Revisit the decision if the closure-table test meets 30 seconds on the full copy with the real write rate, which would keep the system on Postgres.
