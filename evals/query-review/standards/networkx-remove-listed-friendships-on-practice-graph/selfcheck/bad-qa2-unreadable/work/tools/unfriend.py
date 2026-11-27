"""Remove the eight friendships, both directions, and save (NetworkX 3.7 defaults)."""
import json, networkx as nx
p="graphs/practice/social.json"
G=nx.node_link_graph(json.load(open(p)), edges="links")
ids={f"{d['firstName']} {d['lastName']}": n for n, d in G.nodes(data=True) if d.get("kind")=="person"}
U=[("Leopold Ibbotson", "Edda Eskildsen"), ("Dmitri Dovey", "Mira Eskildsen"), ("Jonah Holloway", "Henrik Midgley"),("Bertil Ibbotson", "Mira Kavanagh"), ("Mira Bramwell", "Edda Achterberg"), ("Saga Bramwell", "Kaia Ibbotson"),("Iris Juhl", "Otto Lomax"), ("Greta Midgley", "Rasmus Lomax")]
for a,b in U:
    u,v=ids[a],ids[b]; G.remove_edges_from([(u,v),(v,u)])
json.dump(nx.node_link_data(G), open(p,"w"))
