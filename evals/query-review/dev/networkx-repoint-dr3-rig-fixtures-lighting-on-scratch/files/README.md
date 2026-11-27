# hallb-rig

The lighting rig plan for the Hall B tour (Corvid Stage Lighting Hire): every fixture, the dimmer rack
that feeds it, its DMX universe, and how the racks are powered and fed with data. The plan is a
directed graph stored as NetworkX node-link JSON (`links` key).

- `bin/rig <target> show [node]`: print a summary, or one node and its edges.
- `bin/rig <target> run <script.py>`: load the target's graph, call the script's `run(G)`, save the graph.
- `scripts/fresh_scratch.py`: replace the scratch copy with a fresh copy of the plan.
- `docs/targets.md`, `docs/plan.md`.
