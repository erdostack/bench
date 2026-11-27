Added `litmap/ranking.py` with `reading_list(conn, k=20)`. It returns the ids of the k highest-ranked papers, best first.

- It ranks with `networkx.pagerank` at damping 0.7 (`alpha=0.7`), as `docs/graph/DECISION.md` records. It builds the graph with the existing `litmap.plots.citation_graph`, so it needs no new dependency and no new tables.
- The old `litmap/score.py` is not used. It ran at damping 0.85 and dropped the score of papers with no references.
- Ties are broken by lower paper id, so the order is stable between nightly runs.
- `k` defaults to 20 (the current list length), which is my addition. Pass `k` explicitly to override it.

I checked it on a synthetic 4,800-paper, 31,000-citation database and on a 3-paper toy case. It returns the right number of ids in the expected order. I have not run it on the real `var/library.db`, because that file isn't in the repo.

I did not change `litmap/reading.py`, so `start_here` and its TODO still use the old score until you hook `reading_list` into the page.
