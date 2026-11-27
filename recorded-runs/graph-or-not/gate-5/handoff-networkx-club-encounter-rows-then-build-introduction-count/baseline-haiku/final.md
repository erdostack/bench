I added `introductions(conn, a, b)` in `club/intro.py`. It reuses `member_graph` from `club/graph.py`, so it reads the same encounter data the stats page does.

- It returns 0 when a and b are the same member.
- It returns 0 when a and b have already met directly. A chain a - x - b needs one introduction, so the count is the number of members strictly between a and b on the shortest chain (its encounter count minus one). If you count introductions differently, say so and I will change the `- 1`.
- It returns None when no chain links a and b, or when either id is not a member.

I checked it against the karate club network with an in-memory copy of `db/schema.sql`. All 1,156 ordered pairs matched a direct networkx computation. Example: member 0 to member 33 gives 1 (via member 8). The graph has one connected component, so no pair returns None except for ids that are not members.

I did not touch `club/app.py` or add a route, since you said you would build the panel yourself. The `introductions` function is not yet imported anywhere.
