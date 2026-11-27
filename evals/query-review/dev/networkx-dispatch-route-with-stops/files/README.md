# linehaul

Routing helpers for the parcel network's dispatch screen. The network is a directed graph of depots;
an edge `a -> b` is a scheduled trunk run with its driving time in minutes (runs are often one-way, or
take a different road back).

- `linehaul/load.py`: `load_network(path)` reads an export into a `networkx.DiGraph`
- `linehaul/routes.py`: route helpers used by the dispatch screen
- `data/network.json`: the current network export (about 1,400 depots)
- `tests/`: `python -m unittest discover -s tests` (uses a small hand-made network)
