# seminar-florence

Companion app for the "Families and power in Renaissance Florence" seminar: family pages, a marriage map, and
exercises. The data is Padgett and Ansell's marriage network of the leading families around 1430, as bundled with
networkx (`florentine_families_graph`), plus the Pucci, who had no marriage ties in it.

- Python 3.12, Flask, networkx. SQLite file `var/seminar.db` built by `python -m seminar.load` (not committed).
- Tables in `db/schema.sql`.
