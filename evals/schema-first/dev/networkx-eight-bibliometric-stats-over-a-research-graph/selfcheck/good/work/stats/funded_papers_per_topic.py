def _edges(G, kind):
    """(source, target, attributes) of every edge of this type."""
    return [(u, v, d) for u, v, d in G.edges(data=True) if d.get("type") == kind]


def compute(G):
    """{topic name: funded papers}. Grants point at papers (grant -FUNDED-> Paper); Paper -ABOUT-> topic."""
    funded = {paper for _grant, paper, _ in _edges(G, "FUNDED")}
    out = {}
    for paper, topic, _ in _edges(G, "ABOUT"):
        if paper in funded:
            name = G.nodes[topic]["name"]
            out[name] = out.get(name, 0) + 1
    return out
