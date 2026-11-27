import json
import networkx as nx


def apply(path):
    G = nx.node_link_graph(json.loads(path.read_text()), edges="links")
    for f, rack, d in list(G.in_edges("DR-3", data=True)):
        if d.get("kind") == "fed_by":
            G.add_edge(f, "DR-5", **d)
    G.remove_node("DR-3")
    path.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=1))
