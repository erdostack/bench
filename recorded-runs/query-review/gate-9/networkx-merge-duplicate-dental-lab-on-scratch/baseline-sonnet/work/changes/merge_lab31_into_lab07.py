def change(G, keep="LAB-07", dup="LAB-31"):
    moved = 0
    for u, _, d in list(G.in_edges(dup, data=True)):
        if d.get("kind") == "sent_to":
            G.add_edge(u, keep, **d)
            moved += 1
    G.remove_node(dup)
    return {"moved_sent_to": moved}
