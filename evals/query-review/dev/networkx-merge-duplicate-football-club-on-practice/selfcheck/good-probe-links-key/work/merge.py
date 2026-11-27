import json
import networkx as nx
G = nx.node_link_graph(json.load(open("data/practice.json")))
H = nx.contracted_nodes(G, "CL-0112", "CL-0457")
json.dump(nx.node_link_data(H), open("data/practice.json", "w"))
