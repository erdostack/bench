# Graph decision

Decision: in-process-library

The secretariat wants, for two member organisations, the shortest chain of introductions through shared working groups, about 40 times a day, over 4,200 organisations, 380 working groups and 27,000 memberships. The repo already loads the export into NetworkX 3.7, and the observer-free edge set is at most 21,900 edges, so the chain view belongs in that library and not in Neo4j. Recursive SQL is passed over because nothing shows it holds for shortest-path search (see below).

## Workload facts

- Question asked of the connections: the shortest path between two organisations in a bipartite organisation/working-group graph, to a depth that depends on the data (stated by the user; TODO in consortium/app.py).
- Counts: 4,200 member organisations, 380 working groups, 27,000 memberships of which about 5,100 are observer seats (stated by the user).
- Observer-free edges: 27,000 - 5,100 = about 21,900 (stated counts, subtracted).
- Rules from the secretary-general's office, very clear (stated by the user): observers do not count, so an org cannot introduce or be introduced through a group it only observes; "shortest" means the fewest introductions, and the `weight` column in the export (meetings attended per year, `meetings_per_year` in db/schema.sql) has nothing to do with it; if two chains are equally short either is fine; if there is no chain the view says so.
- Load: the secretariat would use the view maybe 40 times a day (stated by the user) = 40 / 86,400 = about 0.0005 per second. Peak rate unknown.
- Freshness: the CRM export refreshes `var/consortium.db` every night (stated by the user, README.md), so a one-day-old answer is what is shown.
- What is operated today: SQLite file plus Flask, and `consortium/graph.py` already loads the membership export into a NetworkX graph (`networkx==3.7` pinned in requirements.txt). The existing view calls `_graph()` in consortium/app.py, which reloads from SQLite on every request.
- Role is already on each edge (`role`, with `weight` set to meetings attended), so the observer rule is a filter on `role != 'observer'` and the shortest-path call must be unweighted (no `weight=` argument), or the attendance numbers would silently decide the answer.
- Measured (synthetic, not the real data): a random bipartite graph of 4,200 organisations, 380 groups and 27,000 memberships with 5,100 observers, loaded through the repo's own `load_graph`: 27,000 edges, about 11.8 MB traced by tracemalloc (Python 3.x, NetworkX 3.7, run on this machine, sample deleted afterwards; the real graph's shape differs). Load took 0.86 s under tracing, which slows it. After dropping observers 21,900 edges remained, and 200 unweighted `networkx.shortest_path` calls on random pairs took 0.054 s in total, about 0.3 ms each. This is an extrapolation from random data, not a measurement of the real export.
- Tried before: nothing recorded. The repo has no decision record, usage export, slow-query log or migration history.
- unknown: any measurement on the real `var/consortium.db` (there is no copy in the repo; it is gitignored). How the real memberships cluster, for example whether a few big groups connect most organisations. The latency the secretariat would accept (none stated). Peak concurrency, and the memory limit of the Flask process (no deploy configuration in the repo).

## Options considered

- graph-database (Neo4j, as Kasia proposes): rejected, because the edge set is at most 27,000 rows, rebuilt nightly, queried 40 times a day, and the library already in the repo answers a shortest path in well under a millisecond on a same-size synthetic graph. Neo4j would add a second stateful system, a nightly feed from the CRM export and a query language for no gain at this size.
- in-process-library (the export loaded into memory with NetworkX 3.7, already used by the app): chosen, because 27,000 edges is about 11.8 MB in the synthetic run and the nightly refresh is easily met by a reload; the repo already depends on it. The change, described and not applied: build the graph without observer edges, call `networkx.shortest_path(g, a, b)` with no weight (a breadth-first search, so fewest introductions), catch `NetworkXNoPath` and unknown organisation ids and show "no chain", and cache the loaded graph per process instead of reloading it on every request (reload when the file's modification time changes after the nightly export).
- recursive-sql (recursive queries on the SQLite file): rejected, because nothing shows it holds. A shortest path is a search from one organisation outward until the other is found. In SQL that needs a path-carrying recursive query that returns one row per route (so the count can grow quickly through large groups), plus a second pass to pick the shortest, and nobody has run it. The in-process rung holds on the evidence above and is already in the repo.
- no-graph (plain joins, no traversal): rejected, because the chain can be any number of introductions long, so the question follows the relation to a data-dependent depth and is not a join across the link table once.

## What would change the decision

- A measured shortest-path time on the real export, per request including a graph load, above the secretariat's latency budget (the secretariat sets it; none is stated) would be addressed first by caching the loaded graph per process, and only if that is not enough by revisiting the options.
- The loaded graph, measured on the real nightly export with the attributes kept, exceeding the memory limit of the Flask process times the number of worker processes (neither is set in the repo; the platform owner sets them) would move this toward a smaller-footprint structure, not toward Neo4j.
- Memberships growing by orders of magnitude (millions of edges), with a latency budget the library is measured failing, or the export becoming continuous instead of nightly, would reopen graph-database.
- Evidence that a plain SQL query for chains of at most a few introductions meets the secretariat's budget, together with a rule capping the chain length, would make recursive-sql the cheaper rung.
