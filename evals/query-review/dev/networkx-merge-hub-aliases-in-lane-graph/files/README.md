# lanenet

The linehaul lane network of Brightwater Logistics as a NetworkX `DiGraph`: one node per hub, one edge
per directed lane. Built from the merged TMS exports in `data/`.

- `lanenet/graph.py`: `load_graph()` and `load_aliases()`.
- `lanenet/planner.py`: the network planner (checks the graph before it plans).
- `docs/data.md`: what the data means.

Python 3.13, networkx 3.7.
