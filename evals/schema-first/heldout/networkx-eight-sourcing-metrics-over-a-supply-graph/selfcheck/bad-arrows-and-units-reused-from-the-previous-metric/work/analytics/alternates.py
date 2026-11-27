def _edges(G, label):
    """(source, target, attributes) of every edge with this label."""
    return [(u, v, d) for u, v, d in G.edges(data=True) if d.get("label") == label]


def compute(G):
    alt = {}
    for a, b, _ in _edges(G, "alternate_for"):
        alt.setdefault(G.nodes[a]["partNo"], []).append(G.nodes[b]["partNo"])
    return {p: sorted(v) for p, v in alt.items()}
