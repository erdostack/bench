def change(G):
    moved = 0
    for cs, _lab, d in list(G.in_edges("LAB-31", data=True)):
        if d.get("kind") == "sent_to":
            G.add_edge(cs, "LAB-07", **d); moved += 1
    G.remove_node("LAB-31")
    return moved
