import json
import networkx as nx

p = "graphs/practice/network.json"
G = nx.node_link_graph(json.load(open(p)), edges="links")
G.remove_nodes_from([n for n, d in list(G.nodes(data=True)) if d.get("kind") == "sailing" and n.startswith("TRIAL-")])
json.dump(nx.node_link_data(G), open(p, "w"), indent=1)
print(G.number_of_nodes(), "nodes left")
