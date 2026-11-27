import json
from pathlib import Path
import networkx as nx
p = Path("data/scratch/bays.json")
G = nx.node_link_graph(json.loads(p.read_text()), edges="links")
tmp = [n for n, d in G.nodes(data=True) if d.get("kind") == "temporary"]
for n in tmp:
    for m in list(G.neighbors(n)):
        G.remove_edge(n, m)
    G.remove_node(n)
p.write_text(json.dumps(nx.node_link_data(G, edges="links")))
print(len(tmp))
