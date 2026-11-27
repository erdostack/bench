def change(G):
    moved = [(v, dict(d)) for _u, v, d in G.out_edges("RLY-HILLTOP", data=True) if d.get("kind") == "feeds"]
    for v, d in moved:
        G.remove_edge("RLY-HILLTOP", v)
        G.add_edge("RLY-BEACON", v, **d)
