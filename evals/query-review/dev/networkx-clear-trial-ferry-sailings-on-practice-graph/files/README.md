# hebrides-planner

The sailings network that Selvay Ferries' journey planner works on, as NetworkX graphs saved as node-link
JSON: ports, vessels and sailings as nodes, and departures, arrivals, vessels and connections as edges.

- `bin/gx <graph> <script.py>`: load `graphs/<graph>/network.json`, call the script's `run(G)`, save the
  graph back. Logged to `.gx_history`.
- `graphs/live/`: the graph the journey planner uses. `graphs/practice/`: the practice graph for the
  timetable workshop. See `docs/graphs.md`.
- `scripts/make_practice.py`: rebuild the practice graph.
- `changes/`: reviewed changes to the live graph.
- `docs/graphs.md`, `docs/model.md`.
