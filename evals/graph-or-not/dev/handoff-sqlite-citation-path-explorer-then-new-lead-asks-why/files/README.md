# citepath

"How does paper A connect to paper B" explorer for the research office: given two papers, show the shortest chains
of citations between them, skipping retracted papers, optionally only through papers after a given year.

- Python 3.12. The citation snapshot is a SQLite file (`var/snapshot.db`) refreshed daily from the open citation
  dump by `citepath/refresh.py`; it is not committed. Tables in `db/schema.sql`.
- `citepath/paths.py` holds the path search; `sql/` holds queries with `:named` parameters.
