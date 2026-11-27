I added `reading_list(conn, k)` in `litmap/ranking.py`, following the decision in `docs/graph/DECISION.md` (in-process-library): PageRank over the whole citation graph, computed with networkx 3.7 and `alpha=0.7`, which is the PI's damping factor.

- It builds the graph with the existing `citation_graph(conn)` in `litmap/plots.py`, so it reads the `paper` and `cites` tables from the connection you pass in.
- It returns the ids of the top `k` papers, best first. Ties are broken by paper id so the order is stable between runs.
- It returns `[]` for an empty library, and `k` larger than the library returns every paper.

I checked it on a small in-memory SQLite database built from `db/schema.sql`. The ranking came out as expected, and `k=0` and the empty case behaved correctly. I did not touch `var/library.db`, because it is not in the repo.

Things to know before you hook it up:

- I did not change `litmap/reading.py`, which still uses the old `litmap/score.py` loop, so the page will not change until you point it at `reading_list`.
- networkx spreads the score of papers with no references evenly across all papers. The decision record lists this as open: it asked whether the PI wants that behaviour or wants those papers to keep their share. Please confirm with the PI before you rely on the exact scores.
- The real top-20 comparison is still unchecked, because the nightly `litmap/sync.py` database is not in the repo.
