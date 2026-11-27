Decision: graph-database

Adopt the graph database. This is the one case where the evidence points away from staying on Postgres, and your own trial supports it.

Each alternative, against the 30 s contract:
- **Recursive SQL:** 14 minutes forward on a full copy, after Markus's indexing and partitioning. That is about 28 times over the limit, and the work is already done. The queries in `sql/trace_forward.sql` and `sql/trace_backward.sql` are the standard form (`UNION`, id only, indexed on `lot_link`), so there is no obvious rewrite that closes a gap that large. A recursive walk over a fan-out like this reads a large share of 2.3 billion links.
- **In-process library:** it fails on memory. networkx took 19 GB on a 1% sample, so the full graph would be on the order of 1.9 TB, far beyond the 64 GB host limit. A leaner library would use less, but not by the factor of 30 or more you would need. At 3,000 new links a second the in-memory copy would also have to be kept current continuously.
- **No graph:** the question is a transitive closure over chains up to 25 deep, so it does need traversal.
- **Graph database:** 1.2 s forward and 0.9 s backward on a full copy, against 30 s, and it kept up with the MES write rate. That is roughly 25 times of headroom on the contract, with the write rate already tested.

Your boss's preference for Postgres is reasonable, because a second datastore has a real cost. But the cost here is the price of meeting a contractual limit that Postgres demonstrably misses. It is not a matter of taste.

How I'd limit the cost of the second store:
- **Keep Postgres as the system of record.** Run the graph database as a derived store fed from the same MES events. The existing `ingest/mes_consumer.py` already writes `lot_link` idempotently (`ON CONFLICT DO NOTHING`), so a second sink should be idempotent too. That makes it replayable and rebuildable.
- **Only the trace goes through it.** `containment` and `root_cause` in `trace/recall.py` are the only callers that need it, so the integration surface is small. Put the call behind those two functions.
- **Reconcile.** Run a periodic check, for example link counts per plant and per day, between Postgres and the graph store. Contract answers need to be trustworthy, so a drifted store is the main risk.
- **Check the trial results against production conditions.** I can't verify the trial from the repository. Before committing, confirm that it ran with the 3,000 links/s write load and the queries together, on the deepest chains and the widest fan-out lots (a resin lot used in many assemblies), and look at p99 rather than a single run. Also cover operations: backups, failover, upgrade path, and who is on call for it.
- **Check lag.** Containment is only right if the link that connects a suspect lot is already in the store. Decide on and measure the maximum ingest lag, and record it in the runbook for a recall.

I haven't run anything. All performance numbers are from your message, and I read the SQL, schema and ingest code only. The `TODO` in `trace/recall.py` can be resolved by pointing it to this decision once you accept it.
