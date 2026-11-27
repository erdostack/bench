# Graph decision

Decision: in-process-library

The secretariat's liaison chain (the fewest introductions between two member organisations through shared working groups, observers excluded) is a shortest-path question over about 21,900 active memberships, which fits in memory and is answered in well under a millisecond with the networkx library the app already pins. Kasia proposes Neo4j; the recursive-SQL alternative was measured and does not meet the need at depths beyond two, because each level re-expands the whole frontier. The finding it turns on: the graph is small and changes nightly, so a per-request load of 111 ms and a sub-millisecond search are enough for 40 views a day.

## Workload facts

- Member organisations: 4,200 (stated by the user).
- Working groups: 380 (stated by the user).
- Memberships: 27,000 (stated by the user), of which about 5,100 are observer seats (stated by the user). Active memberships (chair or member): 27,000 − 5,100 = 21,900 (derived). Mean active groups per organisation: 21,900 / 4,200 = 5.2; mean active members per group: 21,900 / 380 = 57.6 (derived from the stated counts). Group sizes and the largest hub are unknown.
- Rules from the secretary-general's office (stated by the user): observers do not count; an organisation cannot introduce or be introduced through a group it only observes; "shortest" means fewest introductions; the `weight` column (meetings attended per year) plays no part; equally short chains may return either; no chain must be reported as no chain.
- Schema: one membership row per organisation and group (primary key `(org_id, group_code)`), so an organisation cannot be both observer and member of the same group (`db/schema.sql`). Role values `chair`, `member`, `observer` (`db/schema.sql`).
- Refresh and load: the export refreshes nightly (stated by the user); the view is used about 40 times a day (stated by the user) = 40 / 86,400 = 0.00046 views a second.
- What runs today: `consortium/app.py` calls `load_graph` on every request, which loads all memberships, observer seats included, and stores each membership's `meetings_per_year` in an edge attribute named `weight` (`consortium/graph.py`). Two traps follow: the observer edges must be removed before a search, and any weighted search over that attribute would use meetings, which the rules forbid.
- `requirements.txt` pins networkx 3.7; networkx is already in the app (`requirements.txt`, `consortium/graph.py`).
- Measured, full load: `load_graph` on a synthetic database of 4,200 organisations, 380 groups and 27,000 memberships, Python 3.13 and SQLite 3.53.1, one run: 111 ms per request.
- Measured, in-process search: networkx `shortest_path` without a weight (fewest edges, which is twice the number of introductions) on the 21,900 active edges, 200 random organisation pairs: result matched an independent breadth-first search in 200 of 200 pairs; one pair had no chain; median 0.054 ms, p95 0.22 ms, maximum 4.2 ms. Traced memory for the active graph: about 3.7 MB. The synthetic data is not the CRM export, so these figures show the order of magnitude only.
- Measured, recursive SQL (the candidate rung): a recursive query carrying `(org_id, depth)` with `UNION` and a depth cap of 12, on the same synthetic data. With uniform group sizes: depth 2, 0.13 s; depth 3, 1.2 s; depth 4, 2.3 s. With a skewed hub distribution (largest group 1,417 members): depth 2, 0.8 s; depth 3, 4.3 s; depth 4, 7.3 s. Correctness was checked on one pair only; the query was not validated against the breadth-first search for all pairs. The cost grows because every level re-joins the whole frontier through each group.
- Arithmetic: rows generated per level by recursive SQL are about frontier × 5.2 × 57.6 (about 1.3 million with 4,200 organisations in the frontier), which is repeated work because each organisation is expanded once per depth; the distinct set a correct search must visit is at most 4,200 organisations and 380 groups.
- unknown: the real group-size distribution (the synthetic used both uniform and skewed sizes, neither from the export); the real chain lengths, including the diameter of the active graph (random pairs gave at most 2 introductions on the synthetic); the latency budget for the view (not stated); whether the 4,200 organisations include inactive ones with no memberships; the CRM export itself (not present in the repo; `var/consortium.db` is ignored by git). Looked in: `README.md`, `db/schema.sql`, `consortium/app.py`, `consortium/graph.py`, `requirements.txt`, `.gitignore`.

## Options considered

- graph-database (a dedicated graph store; Kasia proposes Neo4j): rejected, because the active graph is 21,900 edges that a 4 MB in-memory structure searches in under a millisecond, the nightly refresh needs no online writes, and 40 views a day is a trivial load. Adopting Neo4j would add a second store, a nightly sync from the CRM export, and a Cypher dependency for a view that fits in memory.
- in-process-library (the edges loaded into memory): chosen, because the networkx search meets the need on the measured numbers, the library is already pinned and used, and a per-request reload of 111 ms is acceptable at 40 views a day. Build the graph from chair and member rows only, and run an unweighted search so that the `weight` attribute cannot leak into the chain.
- recursive-sql (recursive queries on the database already run): not chosen, because it was measured at 1.2 s (uniform) and 4.3 s (skewed) at depth 3 and does not return the path directly; a correct search would need a visited set that a recursive query cannot keep, so it is not shown to meet the need at the depths the chains may reach.
- no-graph (plain joins, no traversal): rejected, because the chain has no fixed length; the search must follow shared groups to the depth the data reaches.

## What would change the decision

- Observed chain depths in the real export that stay at two introductions or fewer, together with measured recursive-SQL times within the view's latency budget (the budget is not stated; the secretariat sets it), would move this to recursive-sql, since that rung is cheaper.
- Active memberships growing by a factor that pushes the per-request load above the budget, or a requirement to serve the view online many times a second, would move this to a precomputed table refreshed nightly (still in-process), and only then to graph-database; the secretariat owns the load figure.
- A requirement for paths that need the `weight` column, or for weighted routes, changes the search, not the choice, and is excluded by the rules as stated.
