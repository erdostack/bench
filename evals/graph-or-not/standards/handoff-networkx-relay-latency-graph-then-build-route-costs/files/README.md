# relaymesh-ops

Operations tooling for the relay mesh that carries members' messages between regions. The controller publishes
the current topology every 5 minutes as GraphML; the ops box pulls it to `topology/relays.graphml` (not
committed). Nodes are relays (id, site); edges are one-way links with the measured latency.

- `relay/`: ops helpers, one module per tool.
- `docs/routing.md`: what the route report shows.

Python 3.11+, networkx is installed on the ops box (requirements.txt).
