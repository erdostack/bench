"""Planning experiment: LD-15 closed; drop it and re-site its machines at LD-02."""


def run(G):
    moved = 0
    for m, s, d in list(G.edges(data=True)):
        if d.get("kind") == "sited_at" and s == "LD-15":
            G.remove_edge(m, s)
            G.add_edge(m, "LD-02", kind="sited_at")
            moved += 1
    if "LD-15" in G:
        G.remove_node("LD-15")
    return moved
