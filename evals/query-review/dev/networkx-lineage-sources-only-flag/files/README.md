# lineage

Dataset lineage for the warehouse catalogue page. An edge `a -> b` means dataset `b` is built from
dataset `a`.

- `lineage/graph.py`: `load_catalog(path)` and the lineage helpers
- `data/catalog.json`: catalogue export (all datasets and their inputs)
- `tests/`: `python -m unittest discover -s tests`
