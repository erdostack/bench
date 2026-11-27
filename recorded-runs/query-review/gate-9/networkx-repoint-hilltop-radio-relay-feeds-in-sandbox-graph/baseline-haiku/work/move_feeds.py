def change(G):
    moved = [(v, dict(d)) for _u, v, d in G.out_edges("RLY-HILLTOP", data=True) if d.get("kind") == "feeds"]
    for v, _d in moved:
        G.remove_edge("RLY-HILLTOP", v)
    for v, d in moved:
        assert not G.has_edge("RLY-BEACON", v), v
        G.add_edge("RLY-BEACON", v, **d)
    print("moved", len(moved), [v for v, _ in moved])
