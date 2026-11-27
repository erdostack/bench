def _edges(G, label):
    """(source, target, attributes) of every edge with this label."""
    return [(u, v, d) for u, v, d in G.edges(data=True) if d.get("label") == label]


def compute(G):
    suppliers = {}
    for sup, part, _ in _edges(G, "supplies"):
        suppliers.setdefault(part, set()).add(sup)
    return sorted(p for p, s in suppliers.items() if len(s) == 1)
