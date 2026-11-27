# solent-courier-net

The blood courier network of the Solent Blood Service: donor centres, the processing lab, stock depots
and the hospitals we supply, with the drive times between them. Dispatch plans courier runs on it. The
graph is an undirected NetworkX graph stored as GraphML.

- `bin/net <target> show [node]`: a summary, or one node and its routes.
- `bin/net <target> run <script.py>`: load the target's graph, call the script's `run(G)`, write it back.
- `scripts/build_practice_net.py`: build a fresh practice network.
- `docs/targets.md`, `docs/network.md`.
