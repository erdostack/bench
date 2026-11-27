# railnet

The operator's network as a NetworkX graph: stations, their platforms, scheduled runs between platforms
and walking transfers inside stations. `data/network.json` is node-link JSON (`networkx.node_link_graph`,
edges under "links").

- `jobs/`: nightly graph jobs.
- `planner/`: the planners that read the graphs.
- `docs/regional-planner.md`: what the regional planner needs.
