def change(G):
    for u, d in list(G.nodes(data=True)):
        if d.get("level") == "B1" and G.has_edge(u, "DEMO-D2"):
            G.remove_edge(u, "DEMO-D2"); G.add_edge(u, "DEMO-D3", kind="member_of")
