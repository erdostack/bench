I added `liaison_chain(conn, a, b)` in the new file `consortium/liaison.py`. It follows the recorded decision in `docs/graph/DECISION.md`: use NetworkX, which the repo already has, and not Neo4j. I didn't touch the view or `consortium/app.py`.

- **What it returns:** the chain as a list from `a` to `b`, with organisation ids and working-group codes alternating, for example `[1, 'WG-3', 4, 'WG-2', 3]`. It returns `None` if there is no chain, or if either id isn't in the database. If `a == b` it returns `[a]`.
- **Rules from the secretary-general's office:** observer seats are filtered out, so an organisation can't introduce or be introduced through a group it only observes. "Shortest" means the fewest introductions. The `weight` column (meetings attended) is ignored, because the search is unweighted. When two chains are equally short, either one may come back.
- **How it works:** it loads the graph with `consortium.graph.load_graph`, hides the observer edges with a view, and calls `nx.shortest_path` without a weight. It doesn't change `load_graph`, and it reloads the graph on every call. That is fine at about 40 uses a day. If you want it faster, cache the loaded graph per process and reload it when the nightly export changes `var/consortium.db`.
- **Testing:** I tried it on a small in-memory database built from `db/schema.sql`. It handled all of these correctly:
  - an observer-only link is ignored;
  - there is no chain to an organisation reachable only as an observer;
  - the same organisation twice gives `[a]`;
  - an unknown id gives `None`.
- **Not done:** I didn't add a test file, and I didn't run it on the real `var/consortium.db`, because it isn't in the repo.
