Decision: graph-database

Recall tracing should move to a graph database. Your forward recursive query takes 14 minutes on a full copy, 28 times the 30 s contract budget, even after Markus's indexes and partitioning. The graph database trial answered both directions on the full copy in 1.2 s and 0.9 s, and it kept up with the MES write rate.

Numbers the decision turns on:
- Forward on Postgres: 840 s against 30 s. This is your figure, and the walks are up to 25 levels deep, so the rung is measured failing.
- Graph database trial: 1.2 s forward and 0.9 s backward, about 25 and 33 times under the budget.
- In-memory: your networkx sample of 1% took 19 GB, which extrapolates to about 1.9 TB for 2.3 billion links, about 30 times the 64 GB host limit. A compact layout would still need about 18 to 37 GB for one copy before headroom, so the library option does not fit.

Costs of the graph database: a second stateful system to back up, upgrade and be paged for, a feed from the MES and Postgres that can drift (the links grow by about 259 million a day), and a new query language. Postgres stays the system of record for the links.

Before you commit money, run the trial on your real query mix (the largest containment sets, both directions) and at the real write rate for a sustained period, and check the figures are percentiles rather than single runs. Also confirm the freshness the quality team needs.

Your boss's preference for Postgres would hold if someone measured a Postgres remedy on the full copy that brings the forward walk under 30 s (a precomputed closure table is one candidate; its size follows the reachable pairs, which nobody has estimated). Until that is run, the measurement stands.

What I could not find: the lot count and the spread of links per lot, the query plan and row counts for the 14-minute run, the backward timing on Postgres, the number of concurrent traces, and whether the walks prune partitions (they cross plants).

Nothing in the repo was changed. The decision record is at `docs/graph/DECISION.md`.
