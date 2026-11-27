def _edges(G, kind):
    """(source, target, attributes) of every edge of this type."""
    return [(u, v, d) for u, v, d in G.edges(data=True) if d.get("type") == kind]


def compute(G):
    out = {}
    for author, _paper, _ in _edges(G, "WROTE"):
        if G.nodes[author].get("position", 1) == 1:
            name = G.nodes[author]["name"]
            out[name] = out.get(name, 0) + 1
    return out
