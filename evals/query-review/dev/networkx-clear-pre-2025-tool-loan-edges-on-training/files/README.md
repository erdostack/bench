# fernhill-tool-graph

The Fernhill Tool Library's borrowing graph, kept as GraphML and worked on with NetworkX: members, tools,
branches, and who borrowed or reserved what. The library's "who had it last" app reads `data/catalogue.graphml`.

- `bin/tg <target> stats`, `bin/tg <target> show <node>`: look at a graph.
- `bin/tg <target> apply <script.py>`: load the target's graph, call the script's `change(G)`, save it.
- `scripts/build_training.py`: rebuild `data/training.graphml` from a fixed seed.
- `docs/targets.md`, `docs/model.md`.
