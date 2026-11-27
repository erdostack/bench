Decision: in-process-library

Use NetworkX, which is already in the repo (`networkx==3.7`, loaded by `consortium/graph.py`), for the liaison chain view. Do not move the memberships into Neo4j.

The numbers it turns on:
- 27,000 memberships less about 5,100 observer seats leaves about 21,900 edges that count. The export refreshes nightly and the view is used about 40 times a day.
- On a synthetic graph the same size as yours (4,200 organisations, 380 groups, 27,000 memberships, 5,100 of them observers), loaded through your own `load_graph`, I measured about 11.8 MB. 200 unweighted shortest-path searches on random pairs took 0.054 s in total, about 0.3 ms each. This is random data, not your real export, so treat it as an extrapolation.
- Recursive SQL is passed over because nothing shows it holds for a shortest path. It needs a path-carrying query that returns one row per route, and nobody has run one.

How the view should apply the secretary-general's rules (described, not applied):
- Drop edges where `role = 'observer'` before searching, so an organisation cannot introduce or be introduced through a group it only observes.
- Call `networkx.shortest_path(g, a, b)` with no `weight` argument. The graph stores `meetings_per_year` as `weight`, so passing it would let attendance decide the answer, which the office ruled out. Without it the search counts fewest introductions, and either of two equally short chains is fine.
- Catch `NetworkXNoPath` and unknown organisation ids and show "no chain".
- `_graph()` in `consortium/app.py` reloads the whole export on every request. Cache the loaded graph per process and reload when the file changes after the nightly export.

What I could not do:
- There is no copy of `var/consortium.db` in the repo, so I did not measure the real data.
- Nobody has stated a latency budget, peak concurrency or the Flask process memory limit.
- Real memberships may cluster differently from my random sample, for example a few very large groups.

Nothing in the repo was changed apart from the new `docs/graph/DECISION.md`. My scratch measurement files were removed. The TODO in `consortium/app.py` is untouched.
