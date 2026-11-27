def _edges(G, kind):
    """(source, target, attributes) of every edge of this type."""
    return [(u, v, d) for u, v, d in G.edges(data=True) if d.get("type") == kind]


def compute(G):
    """{author name: first-author papers}. The author order is `position` on the WROTE edge."""
    out = {}
    for author, _paper, d in _edges(G, "WROTE"):
        if d["position"] == 1:
            name = G.nodes[author]["name"]
            out[name] = out.get(name, 0) + 1
    return out
