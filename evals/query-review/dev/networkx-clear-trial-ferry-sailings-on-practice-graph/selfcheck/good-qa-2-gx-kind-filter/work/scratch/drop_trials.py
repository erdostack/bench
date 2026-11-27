def run(G):
    gone = [n for n in list(G.nodes) if G.nodes[n].get("kind") == "sailing" and str(n).split("-", 1)[0] == "TRIAL"]
    G.remove_nodes_from(gone)
    return len(gone)
