drainage/upstream.py loads the network into networkx, removes pumping stations (rule in
docs/adr/0003-upstream-trace.md) and returns the sorted ancestors of the node.
