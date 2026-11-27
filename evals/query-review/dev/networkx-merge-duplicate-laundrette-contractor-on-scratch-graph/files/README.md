# van-planner

Plans the engineers' van rounds for Spinwell Laundrettes' machine contractors: which contractor visits
which shops, in what order. It works on a graph of shops, machines, contractors and depots.

- `data/scratch-graph.json`: the graph the planner and its tests run on (NetworkX node-link JSON, directed).
- `scripts/rebuild_scratch.py`: rebuild `data/scratch-graph.json` from `fixtures/`.
- `bin/scratch <change.py>`: load the scratch graph, call the file's `run(G)`, save it, print the result.
- `bin/plan`: print the van rounds from the scratch graph.
- `docs/graph.md`: the graph's shape and where it comes from.
