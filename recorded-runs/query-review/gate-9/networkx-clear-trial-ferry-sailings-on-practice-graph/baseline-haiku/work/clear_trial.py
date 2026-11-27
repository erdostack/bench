def run(G):
    trial = [n for n, d in G.nodes(data=True) if d.get("kind") == "sailing" and str(n).startswith("TRIAL-")]
    G.remove_nodes_from(trial)
    return len(trial)
