# swapboard

The Ashby Road Allotments Association's seed swap as a graph: members, the varieties they pledge and
bring, and the yearly swap days. SQLite, one database: `data/swap.db`.

- `bin/swapq [--db <path>] "<sql>"`: run SQL (default database `data/swap.db`).
- `bin/apply [--db <path>] changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, `NNNN_<what>.py`.
- `docs/data-changes.md`: how data is changed. `docs/model.md`: what is in the graph.
