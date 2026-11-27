"""Remove the TRIAL- sailings the workshop left (removing a node removes its edges)."""


def run(G):
    trial = [n for n, d in G.nodes(data=True) if d.get("kind") == "sailing" and n.startswith("TRIAL-")]
    G.remove_nodes_from(trial)
    return len(trial)
