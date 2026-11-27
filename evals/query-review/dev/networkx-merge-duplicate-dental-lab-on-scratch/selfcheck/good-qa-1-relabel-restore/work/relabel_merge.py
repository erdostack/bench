import networkx as nx
p = "scratch/labs.graphml"
G = nx.read_graphml(p)
keep = dict(G.nodes["LAB-07"])
nx.relabel_nodes(G, {"LAB-31": "LAB-07"}, copy=False)
G.nodes["LAB-07"].clear(); G.nodes["LAB-07"].update(keep)
nx.write_graphml(G, p)
