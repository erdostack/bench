import json
import networkx as nx
p = "graphs/practice/network.json"
with open(p) as f:
    G = nx.node_link_graph(json.load(f), edges="links")
trial = {n for n, d in G.nodes(data=True) if d.get("kind") == "sailing" and n.startswith("TRIAL-")}
G.remove_edges_from([(u, v) for u, v in G.edges() if u in trial or v in trial])
G.remove_nodes_from(trial)
with open(p, "w") as f:
    json.dump(nx.node_link_data(G, edges="links"), f, indent=1, sort_keys=True)
print(len(trial), "removed")
