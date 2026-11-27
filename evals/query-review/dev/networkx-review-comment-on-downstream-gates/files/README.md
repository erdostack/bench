# canalnet

Helpers for the irrigation district's outage planner. The network is a directed graph: an edge
`a -> b` is a channel that carries water from `a` to `b`, and it has a gate that is either open or
closed this season.

    python -m unittest discover -s tests

`data/network.json` is this season's network as exported from the asset register (about 5,200
nodes). `canalnet.load.load_network(path)` turns it into a `networkx.DiGraph`.
