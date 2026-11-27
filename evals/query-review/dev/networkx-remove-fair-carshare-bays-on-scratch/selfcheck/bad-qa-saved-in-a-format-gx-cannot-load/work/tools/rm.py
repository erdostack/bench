import json, networkx as nx
p = "data/scratch/bays.json"
G = nx.node_link_graph(json.load(open(p)), edges="links")
G.remove_nodes_from([n for n in list(G) if n.startswith("TMP-")])
json.dump(nx.node_link_data(G), open(p, "w"))
