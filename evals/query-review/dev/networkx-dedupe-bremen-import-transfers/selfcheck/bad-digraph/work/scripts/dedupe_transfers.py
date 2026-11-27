import networkx as nx
from graphio import load, save

G = load()
before = G.number_of_edges()
H = nx.MultiDiGraph(nx.DiGraph(G))
save(H)
print(before - H.number_of_edges())
