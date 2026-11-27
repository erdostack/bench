drainage/upstream.py: loads the pipes into a networkx DiGraph, drops the pumping stations (the rule in
docs/graph/DECISION.md is that the trace stops there), and returns the sorted ancestors of the node.
