def change(G):
    for _, t, d in [e for e in G.out_edges("RLY-HILLTOP", data=True) if e[2]["kind"] == "feeds"]:
        G.add_edge("RLY-BEACON", t, **d)
        G.remove_edge("RLY-HILLTOP", t)
