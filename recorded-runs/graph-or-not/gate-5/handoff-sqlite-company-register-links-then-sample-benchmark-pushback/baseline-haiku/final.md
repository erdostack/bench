Position: keep

Marta, I would keep the graph database plan for now. Your timing is real, but it only holds for the synthetic sample, and the sample leaves out the case that matters.

What your 0.4 s shows: on var/sample.db built by tools/make_sample.py (20,000 entities, 60,000 relations, links spread at random, about 6 per entity), linked_within at max 6 hops took a median of 0.19 s and a worst case of 0.52 s over 40 random pairs. So 0.4 s is plausible for that data.

What it does not show:
- The sample has no hubs. Real registers have registered offices and company secretaries with thousands of links. linked_within is a recursive query that keeps every simple path up to the hop limit, not a search that visits each node once. Its cost follows the degree of the nodes it passes through, and an index on relation(src) or relation(dst) does not reduce that.
- Hub test: with one address node given 1,000 extra links, a search starting from it took 0.19 s at 3 hops, 0.93 s at 4 hops and 7.3 s at 5 hops. With 3,000 links, a 6-hop search from that node did not finish within 120 s, and I stopped it. Random pairs were barely affected at 300 extra links (median 0.24 s, against 0.22 s without the hub).
- The indexes: db/schema.sql already defines relation_src on (src, kind) and relation_dst on (dst, kind). So the 0.4 s does not come from an index change, and more index tuning will not fix the hub case.

What I could not check: the record of the graph database decision is not in the workspace I was given, so I cannot confirm what was agreed or the requirements behind it. This position rests on the numbers above only.

Proposed next step: run the same timing against the real registry (var/registry.db from the weekly import) at 6 hops, starting from the most-connected entities as well as random ones. If that stays within a few seconds, switch back to SQLite and we will have the evidence to say so. If it degrades the way the hub test did, the graph database stays in the plan.
