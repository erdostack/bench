Decision: not recorded in this repository

I could not find what we decided for the citation-path explorer, so I cannot say the decision or the numbers behind it. Nothing in the repo records a decision, a benchmark, a target, or a choice of store. The README, `db/schema.sql`, `sql/path.sql`, and `citepath/` show only the current code, not the reasoning for it. Before pasting anything to Marisol, someone who was in that decision should confirm the category and the figures.

What the code does now, which bears on her question:
- The data lives in SQLite. `citepath/config.py` points to `var/snapshot.db`, which `citepath/refresh.py` rebuilds daily from the open citation dump, so the snapshot is SQLite-backed like the rest of the repo.
- The path search does not query SQLite at request time. `citepath/paths.py` loads the whole citation table into a networkx graph the first time it is used in each worker, and runs `nx.all_shortest_paths` on that in-memory graph. `config.py` sets 6 workers, so the full graph is loaded up to six times. The repo records no graph size or memory figure, so I cannot say what that costs.
- `sql/path.sql` is a recursive-CTE prototype that is not used by the Python code. It is the only place in the repo that filters retracted papers.
- `citepath/paths.py` does not implement the behaviour the README describes. It does not skip retracted papers and does not apply the optional year filter. Any decision that assumed the explorer already does both is resting on code that is not here.

So the accurate position for Marisol is: the snapshot is SQLite, but the search runs in memory on a whole-graph load, and the retracted-paper and year-filter rules are described in the README but not implemented in `paths.py`. Whether the team should keep that design is a separate question the repo cannot answer.

I did not change any decision record.
