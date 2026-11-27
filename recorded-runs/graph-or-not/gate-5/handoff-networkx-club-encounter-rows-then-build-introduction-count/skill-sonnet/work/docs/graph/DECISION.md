# Graph decision

Decision: recursive-sql

The question was how many introductions lie between a newcomer's buddy and a senior member, counting only ties where two members met in at least 3 contexts, and whether that needs Neo4j, the networkx we already use, recursive SQL on the SQLite file, or no graph. It is a walk from one member of data-dependent depth, over at most 200 members, and a recursive query on the SQLite file already in use returned the same answers as networkx in a measurement (34 members, 1,156 member pairs, 0 mismatches, about 0.3 ms per lookup). Neo4j would be a second store for about 50 lookups a day.

## Workload facts

- Question asked of the connections: shortest number of hops between two members over ties of the same kind (member to member), a walk of data-dependent depth (request in club/app.py TODO; encounter table in db/schema.sql).
- Stated by the user: the welfare lead's rule is that a tie counts as an introduction only if the two members met in at least 3 contexts; pairs that met in one or two contexts are not a link at all. Count rows per pair: `GROUP BY member_a, member_b HAVING COUNT(*) >= 3`.
- Stated by the user: the demo club is the karate club data, 34 members, 78 ties, 231 encounter rows (one per context a pair met in).
- Stated by the user: real clubs on the platform are under 200 members.
- Stated by the user: about 50 lookups a day.
- Stated by the user: Rafael wants to move the member network into Neo4j because "introductions are a graph problem".
- Measured on a rebuilt demo database (python3 and sqlite3 3.53.1, networkx 3.7, scratch in memory, nothing written to the repo): 34 members, 78 distinct pairs, 231 encounter rows (matches the numbers stated).
- Measured: 48 of the 78 ties have 3 or more contexts, so the rule removes 30 of 78 ties (same run, `HAVING COUNT(*) >= 3`).
- Measured: with the rule applied, the demo club splits into one component of 28 members and 6 members with no qualifying tie; 366 of 1,156 ordered pairs (34 x 34) have no path (same run). Without the rule, all 34 members are connected. The panel needs a "no introduction path" answer.
- Measured: a recursive query (breadth walk over the qualifying ties, depth capped at 10) agreed with `nx.shortest_path_length` on all 1,156 pairs, 1,156 lookups took about 0.32 s in total (about 0.3 ms each).
- Measured on a synthetic 200-member club (a preferential-attachment graph with 591 ties and 2,709 encounter rows, denser than the demo): the same query took about 7.6 ms on average and 38.6 ms at the slowest over 200 random pairs. This is synthetic, not platform data.
- Load: 50 lookups a day against 7.6 ms each is under half a second of work a day.
- Existing code: club/graph.py builds an `nx.Graph` from every encounter row with no threshold, so it would count every tie; it feeds the stats page and would need the same filter before it was reused for this panel (club/graph.py).
- What is operated today: SQLite (`var/club.db`), Flask, networkx 3.7 (README.md, requirements.txt, club/app.py).
- unknown: write rate and how fresh the panel must be; the repo has no usage data on how often encounters are added.
- unknown: the real platform's tie counts and fan-out for clubs near 200 members; only the demo club is in the repo, and the 200-member run above is synthetic.

## Options considered

- graph-database (Neo4j, as Rafael proposes): rejected, because the graph has under 200 members and about 50 lookups a day, and the recursive query on the file already in use answers in milliseconds (measured above), so a second store to run and keep in sync is not needed.
- in-process-library (networkx, already a dependency): rejected as the first choice only because the cheaper rung holds; it would also work (the edges fit in memory for fewer than 200 members), and it is the fallback if the recursive query is ever not fast enough or the team prefers to keep path logic in Python. Filter the ties to those with 3 or more contexts in both cases.
- recursive-sql (recursive query on SQLite): chosen, because it was measured correct against networkx on all 1,156 demo pairs and takes about 0.3 ms per lookup on the demo and about 7.6 ms on average on a synthetic 200-member club. Use `UNION` (not `UNION ALL`) so a member is visited once, add both directions of each tie, cap the depth, and return "no path" when the target is not reached.
- no-graph (plain joins): rejected, because "how many introductions" is a path of unknown length between two members, not a lookup across a link table.

## What would change the decision

- A real club's lookups on its own data taking longer than the panel's budget (the product owner sets it; none is stated) would move this to in-process-library.
- Clubs growing well beyond 200 members, or lookups growing from about 50 a day to many a second with a latency budget the query misses when measured on the real tie data, would move this toward in-process-library first, and graph-database only if that fails too.
- The welfare lead changing the rule from 3 contexts to another count would not change the option, only the `HAVING` value.
