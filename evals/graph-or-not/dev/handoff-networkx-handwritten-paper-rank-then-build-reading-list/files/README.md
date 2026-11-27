# litmap

The lab's literature tool: the shared library of papers we have read or cite, with their references, a few
plots, and the "start here" reading list for new lab members.

- Python 3.12, SQLite (`var/library.db`, rebuilt nightly from the reference manager export by `litmap/sync.py`,
  not committed). Tables in `db/schema.sql`.
- `litmap/score.py` computes the importance score behind the reading list.
- networkx is used by `litmap/plots.py`.
