# monorepo-buildgraph

The monorepo's target graph, extracted nightly from the BUILD files, as a NetworkX DiGraph saved to
`graph/targets.json` (node-link JSON). The build dashboard, the "who uses this" lookups and the
deletion bot read it.

- `tools/graphio.py`: load and save. `tools/refresh.py`: the nightly refresh.
- `docs/BUILD_GRAPH.md`: what nodes, edges and attributes mean. `docs/tickets.md`: open tickets.
