Decision: in-process-library

Keep networkx, which the app already uses. At under 200 members and about 50 lookups a day, a shortest-path query over an in-memory graph is instant. Neo4j would mean a second datastore to run and keep in sync, and the SQLite file stays the source of truth. Recursive SQL would work, but it is harder to read and to test than `nx.shortest_path_length`. This is a graph problem, but a very small one.

What I did:
- `club/graph.py`: added `vouching_graph(conn)`. It keeps only pairs with at least 3 rows in `encounter`, and the 3 is the constant `MIN_CONTEXTS`. It also adds `introductions(conn, buddy, senior)`, which returns the shortest-path length over that graph, or `None` if no chain of vouching ties connects them. An unknown member id raises `KeyError`.
- `club/app.py`: replaced the TODO with `GET /api/buddy-panel/<buddy>/<senior>`. It returns `{"buddy", "senior", "introductions"}`, with `introductions` null when there is no chain, and 404 for an unknown member.
- The existing stats page still counts every tie. I left it alone, so it and the panel will show different tie counts.

Check: I built the demo DB and ran the endpoint through the Flask test client. Of the 231 encounter rows, 48 pairs meet the 3-context rule. For members 0 and 33 the answer is 2, and an unknown id gives 404. I didn't add a test file, and I removed the generated `var/` folder afterwards.

Things to confirm:
- The schema has no seniority field, so the endpoint takes the senior member's id as a parameter. The panel needs a way to pick the senior member.
- Under the 3-context rule the network may split into disconnected pieces, so some buddy and senior pairs will legitimately return null. The panel should show that as "no vouched route" and not as 0 or an error.
