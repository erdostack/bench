Added fission/split.py: split_cost(conn, a, b) builds the club graph with each tie's contexts as its
capacity and returns networkx's minimum cut value, i.e. the smallest total contexts that disconnects a
from b (the rule in docs/graph/DECISION.md). For 0 and 33 that is 22.
