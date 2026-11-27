import json
from pathlib import Path

import networkx as nx

p = Path("data/practice.json")
G = nx.node_link_graph(json.loads(p.read_text()))
G = nx.contracted_nodes(G, "CL-0112", "CL-0457", self_loops=False)
p.write_text(json.dumps(nx.node_link_data(G)))
