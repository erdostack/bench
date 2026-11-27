# graintrack

Grain flows between traders (farm sellers, elevators, merchants, mills) for the market report: who sold
grain to whom this season, and how much. NetworkX 3.x, plain Python.

- `flows/io.py`: `load_flows()` reads `data/flows.json` into a DiGraph.
- `flows/report.py`: the weekly market report.
- `data/duplicate_pairs.csv`: traders the matcher thinks are the same business.
- `docs/flows.md`: the graph and the merge rules.
