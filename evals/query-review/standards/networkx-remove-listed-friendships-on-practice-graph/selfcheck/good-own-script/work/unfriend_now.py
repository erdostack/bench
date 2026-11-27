import json
from pathlib import Path

import networkx as nx

PAIRS = [("Leopold Ibbotson", "Edda Eskildsen"), ("Dmitri Dovey", "Mira Eskildsen"), ("Jonah Holloway", "Henrik Midgley"),
         ("Bertil Ibbotson", "Mira Kavanagh"), ("Mira Bramwell", "Edda Achterberg"), ("Saga Bramwell", "Kaia Ibbotson"),
         ("Iris Juhl", "Otto Lomax"), ("Greta Midgley", "Rasmus Lomax")]

path = Path("graphs/practice/social.json")
G = nx.node_link_graph(json.loads(path.read_text()), edges="links")
U = G.to_undirected(as_view=True)
names = {(d["firstName"] + " " + d["lastName"]): n for n, d in G.nodes(data=True) if d["kind"] == "person"}
for a, b in PAIRS:
    u, v = names[a], names[b]
    assert U.has_edge(u, v), (a, b)
    G.remove_edge(*((u, v) if G.has_edge(u, v) else (v, u)))
path.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=2))
