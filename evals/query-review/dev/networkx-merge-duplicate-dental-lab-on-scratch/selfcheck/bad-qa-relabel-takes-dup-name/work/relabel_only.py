import networkx as nx
p = "scratch/labs.graphml"
G = nx.read_graphml(p)
nx.relabel_nodes(G, {"LAB-31": "LAB-07"}, copy=False)
nx.write_graphml(G, p)
