# winter-roads

Scripts for the council's winter road plan. The highways GIS exports `var/roads.db` (not committed; tables
in `db/schema.sql`) every autumn and after major roadworks.

- `python -m winter.report` writes the plough priority list, `var/priority.csv`, for the depot.
- Python 3.12, standard library only so far.
