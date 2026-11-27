import json
from pathlib import Path

import networkx as nx

path = Path("graphs/practice/network.json")
G = nx.node_link_graph(json.loads(path.read_text()), edges="links")
G.remove_nodes_from([n for n in list(G) if str(n).startswith("TRIAL-")])
path.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=2))
print(G.number_of_nodes())
