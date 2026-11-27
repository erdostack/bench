def prune(G):
    referenced = {label for n in G for label in G.nodes[n].get("data", [])}
    unused = sorted(n for n in G if n.startswith("//legacy/") and G.in_degree(n) == 0 and n not in referenced)
    G.remove_nodes_from(unused)
    return unused
