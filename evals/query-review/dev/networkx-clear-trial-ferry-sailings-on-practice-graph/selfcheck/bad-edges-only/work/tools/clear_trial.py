def run(G):
    trial = [n for n in G if n.startswith("TRIAL-")]
    G.remove_edges_from([e for e in G.edges() if e[0] in trial or e[1] in trial])
    return len(trial)
