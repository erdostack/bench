# florence-families

Teaching site for the Renaissance Florence unit: family pages and the marriage network of the leading families
around 1430 (Padgett and Ansell's data, as bundled with networkx as `florentine_families_graph`; the Pucci, who
had no marriage ties in the data, are listed too).

- Python 3.12, Flask, SQLite (`var/florence.db`, built by `python -m florence.load`, not committed).
- Tables in `db/schema.sql`.
