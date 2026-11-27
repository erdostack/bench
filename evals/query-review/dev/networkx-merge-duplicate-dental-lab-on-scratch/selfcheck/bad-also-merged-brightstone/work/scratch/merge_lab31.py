def change(G):
    dups = [n for n, d in G.nodes(data=True) if d.get("kind") == "lab" and n != "LAB-07" and d["name"].lower().startswith("bright")]
    for dup in dups:
        for cs, _l, d in list(G.in_edges(dup, data=True)):
            G.add_edge(cs, "LAB-07", **d)
        G.remove_node(dup)
