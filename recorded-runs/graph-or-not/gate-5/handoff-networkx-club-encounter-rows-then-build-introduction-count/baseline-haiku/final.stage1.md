Decision: in-process-library

Keep the member network in memory and use networkx, which the project already depends on (networkx==3.7 in requirements.txt and used by club/graph.py). Do not move the network into Neo4j.

Why:
- The question "how many introductions from the buddy to a senior member" is a shortest-path (hop count) query, so it is a graph problem. But the data is tiny: 34 demo members, 78 ties, 231 encounter rows, real clubs under 200 members, about 50 lookups a day. Loading the whole network per request, or caching it at startup, costs milliseconds. A dedicated graph database adds a second service, a second data store to keep in step with var/club.db, and operating cost, for no measurable gain.
- Recursive SQL on the SQLite file could also answer this, but a bounded recursive CTE for shortest hop count is harder to write and check than a single networkx call, and it would duplicate the tie-filtering logic in SQL. Neither option is wrong; the library is simpler and already in use.
- Rafael's premise is right that this is a graph problem, but that does not by itself justify a graph database.

Implementation notes for the buddy panel in club/app.py:
- Apply the welfare rule before building the graph. A tie counts only if the pair has at least 3 encounter rows. Use SELECT member_a, member_b FROM encounter GROUP BY member_a, member_b HAVING COUNT(*) >= 3, and add those edges to a new graph. Do not change member_graph or stats(): they count every tie, and changing them would alter the stats page.
- Hops = nx.shortest_path_length(g, buddy, senior) on that filtered graph. Return a clear "no chain" result when there is no path (nx.NetworkXNoPath) or when either id is not a member (nx.NodeNotFound).
- Test with fixtures: a pair that met in exactly 2 contexts must not create a link; a pair that met in 3 must; buddy equal to senior gives 0 introductions.

Caveat: this decision uses the schema, the loader and the stated sizes in this workspace. The live club data was not checked, and the welfare rule itself was not reviewed here.
