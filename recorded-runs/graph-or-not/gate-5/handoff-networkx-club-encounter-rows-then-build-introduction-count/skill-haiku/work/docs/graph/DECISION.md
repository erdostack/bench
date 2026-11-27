# Graph decision

Decision: in-process-library

The welfare officers ask how many introductions take a newcomer's buddy to a senior member, counting only ties where the two members met in at least 3 contexts, and Rafael proposes Neo4j. The walk is short and the graph is tiny: the demo club has 48 ties that pass the rule (of 78), at most 19,900 pairs for a club of 200 members, and a breadth-first walk in the graph library already in the app answers any lookup in well under a millisecond on that bound, so no store is needed. The finding it turns on is the route count of a recursive SQL walk, which grows with fan-out and needs a depth cap nobody has set.

## Workload facts

- The question asked of the connections is the shortest number of ties from one member to another over the filtered graph, i.e. a walk of unknown depth from a starting point (`club/app.py`, TODO: "how many introductions from the newcomer's buddy to a senior member"; no buddy query runs yet, so this is the request's definition).
- The rule: a tie counts as a link only if the two members met in at least 3 contexts; a pair with 1 or 2 contexts is not a link at all (stated by the user, the welfare lead).
- Demo club: 34 members, 78 ties, 231 encounter rows, one row per context (stated by the user; `README.md` names the karate club; `club/load.py` expands each tie's weight into one row per context, and the sum of weights is 231, measured with `networkx.karate_club_graph()` 3.7 on Python 3.13.18).
- Ties passing the rule: 48 of 78 (measured on the bundled karate club graph, weight at least 3). Weight histogram of the 78 ties: 6 at 1, 24 at 2, 27 at 3, 12 at 4, 7 at 5, 1 at 6, 1 at 7 (measured).
- Filtered graph: 6 members with no tie passing the rule, 7 connected components, 378 of 561 member pairs reachable (measured). Shortest path lengths over reachable pairs: 1 to 7 introductions, with 48, 100, 94, 74, 45, 15 and 2 pairs at 1 to 7 (measured). Diameter of the filtered graph: 7 (measured).
- Size of a real club: under 200 members (stated by the user). Largest possible pairs: C(200, 2) = 19,900 (arithmetic). Ties in a real club: unknown; the repo has no real club data.
- Fan-out: demo filtered graph average 2 x 48 / 34 = 2.8 ties per member (arithmetic from the measured counts); real-club fan-out unknown.
- Measured in memory, `networkx` 3.7 on Python 3.13.18, `tracemalloc`: a 200-member complete graph with 19,900 edges (the bound) takes 3.17 MB, 159 bytes per edge; single-source shortest path lengths on it take about 0.06 ms per lookup. On the filtered demo graph, about 0.008 ms per lookup.
- Recursive SQL checked on SQLite 3.53.1 (in-memory copy built from the karate data with `db/schema.sql`, not the repo file, which is not built): a recursive walk with `UNION` on (member, depth) and a depth cap of 7 returned the same minimum introduction counts as networkx for all 34 starting members (measured). It produced 3,896 walk rows across the 34 starts, about 115 per start, and about 13 ms per start including a second counting pass (measured). The rows grow with fan-out to the depth, and no depth cap is set in the repo; with real-club fan-out unknown, the row count at real size is not shown.
- Load: about 50 lookups a day (stated by the user); no latency budget stated, and the single-process load is far below any budget measured above.
- Writes and freshness: not stated. `club/graph.py` rebuilds the graph from the tables on every stats call, so the buddy lookup can do the same.
- What is operated today: SQLite `var/club.db` built by `python -m club.load` (`README.md`); Flask app (`requirements.txt`, `flask==3.1.*`); `networkx==3.7` pinned in `requirements.txt` and used by `club/graph.py` for the stats page. No graph database is run or named in the repo.
- What is already in the stats page: `club/graph.py` counts all 78 ties and does not apply the 3-context rule, so the existing stats page does not reflect the welfare rule (read from the code).
- unknown: real club data (fan-out, members per club, ties per pair) is not in the repo; the required maximum introduction count for the panel is not stated (the answer is data-dependent); the freshness and latency requirement for the panel is not stated; the buddy and senior member IDs for a real request are not in the repo.
- What was tried and what happened: unknown. No decision record, changelog or migration exists in the repo.

## Options considered

- graph-database (Neo4j, as Rafael proposed): rejected, because the profile is absent: the graph is at most 19,900 pairs and about 3 MB in memory, the walk runs about 50 times a day, nothing is measured failing, and a second stateful server with its own load step would cost more than the lookup it serves.
- in-process-library (the graph library already in the app, networkx 3.7, loaded from the tables): chosen, because it is shown to meet the need at the club bound (0.06 ms per lookup on 19,900 pairs, 3.17 MB measured), it needs no depth cap to find the shortest count, and it is already a pinned dependency. The rule is applied by building the graph from only ties whose encounter count is at least 3.
- recursive-sql (recursive queries on the SQLite file): passed over for now, because the demo check is correct and fast, but the walk's row count grows with fan-out to the depth, the cap is not set anywhere in the repo, and the real-club fan-out is unknown, so it is not shown to meet the need at a real club's size. It is not disproved; it would become the answer if the owner set a depth cap and a real club's walk rows were measured to fit.
- no-graph (plain joins, no traversal): rejected, because the number of introductions follows ties through other members at unknown depth; a join with a fixed number of steps would not give the shortest count.

## What would change the decision

- A measured real-club walk, with the same rule applied, showing the recursive walk's row count under the owner's depth cap staying within the budget the owner sets (for example, rows per start and milliseconds per lookup on the real club file) would move this to recursive-sql. The budget is the welfare team's to set; the repo sets none.
- A real club whose filtered graph is far above the 200-member bound (the bound is stated by the user), or a requirement for many more lookups a day (for example, one per member per day for all members) with a latency budget the in-process load cannot meet, measured on that club's data, would move this toward recursive-sql or a store; the thresholds are the owner's to set.
- A requirement to share one live graph between several processes that must see tie changes within seconds, with the graph too large for a copy per process, would move this to a dedicated store; no such requirement is stated.

Nothing in the repo was changed.
