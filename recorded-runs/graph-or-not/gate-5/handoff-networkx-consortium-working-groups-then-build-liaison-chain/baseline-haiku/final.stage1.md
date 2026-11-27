Decision: in-process-library

Use the networkx graph that `consortium/graph.py` already builds, and run an unweighted shortest path in the Flask view. A graph database is not needed for a graph of this size, and the repo already has the library.

Why:
- The graph is small. About 4,200 organisations and 380 working groups make roughly 4,580 nodes, and the non-observer memberships make about 22,500 edges. On a synthetic export of that size, 40 shortest-path queries ran in about 2 ms in total, and every pair I tried returned a path or a clean no-path result. That is far below the 40 views a day the secretariat needs.
- Shortest chains with the actual path are a graph search. SQL can do it with a recursive query, but returning the path and handling the bipartite org/group alternation and loops is clumsy there. networkx does it in one call.
- The export refreshes nightly, and the graph is rebuilt from SQLite on each request in `app.py`. A graph database would add a sync step to that without any gain.

What the view has to do differently from the current code:
- `load_graph` loads every membership, observers included. The liaison view must remove `role = 'observer'` edges before it searches, because the secretary-general's office says observers never count. Build a filtered copy of the graph and search that. Do not search the loaded graph directly, or an observer seat will create a chain.
- Do not pass `weight="weight"` to `shortest_path`. The weight is meetings per year and is not part of the rule. Leave the search unweighted so the result is the fewest groups.
- The number of introductions is `(len(path) - 1) // 2`, since the path alternates organisation, group, organisation. A chain of one shared group is one introduction.
- If `networkx.NetworkXNoPath` is raised, the view should say that no chain exists. If the two organisations are the same, handle that as its own case.
- Any tie is acceptable, so the first path networkx returns is fine.

Open points:
- The existing `/orgs/<id>/groups` endpoint also uses the full graph, so it lists groups where an organisation only observes. Confirm with the secretariat whether that endpoint should change, since the same rule may apply there.
- The timings are from synthetic data. Check the view against the real `var/consortium.db` before relying on it.

Why not the other options:
- graph-database: a separate service to keep in step with a nightly export does not pay off for a graph this size.
- recursive-sql: shortest path with the actual chain and the observer filter is possible in SQL, but it is awkward and harder to check than the library call.
- no-graph: the problem is a path search through shared groups, which is a graph traversal.
- need-more-information: the rules are settled and the data store is not the open question.
