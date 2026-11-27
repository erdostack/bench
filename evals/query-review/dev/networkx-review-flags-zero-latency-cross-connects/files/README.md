# fabric-latency

Latency figures for the tenant SLA dashboard, computed over the data-centre fabric graph.

- `data/fabric.json`: devices and links (servers, patch panels, top-of-rack switches, spines, super-spines).
- `fabric/latency.py`: `load_fabric()` and `one_way_latency(G, a, b)`.
- `docs/fabric.md`: what the numbers mean.
