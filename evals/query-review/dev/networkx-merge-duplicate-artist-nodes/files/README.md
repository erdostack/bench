# collab-graph

Who-recorded-with-whom graph for the label's catalogue, built with NetworkX 3.7.

- `collab/graph.py`: `load()` reads `data/collaborations.json` into an undirected `nx.Graph`.
- `collab/report.py`: the collaborator report (most-connected artists, strongest partnerships).
- `docs/graph.md`: what nodes, edges and attributes mean.
