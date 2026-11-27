"""Try the removal on live to see the counts (the edges are put back before the graph is saved)."""

def run(G):
    gone = [(u, v, d) for u, v, d in G.edges(data=True) if d["kind"] == "knows"][:3]
    G.remove_edges_from([(u, v) for u, v, _d in gone])
    G.add_edges_from(gone)
    return len(gone)
