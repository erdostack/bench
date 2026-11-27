import networkx as nx


def change(G):
    G.remove_edge("LAB-31", "CITY-01")
    for cs, lab, d in list(G.edges(data=True)):
        if lab == "LAB-31" and d["kind"] == "sent_to":
            G.remove_edge(cs, lab)
            G.add_edge(cs, "LAB-07", **d)
    assert G.degree("LAB-31") == 0
    G.remove_node("LAB-31")
