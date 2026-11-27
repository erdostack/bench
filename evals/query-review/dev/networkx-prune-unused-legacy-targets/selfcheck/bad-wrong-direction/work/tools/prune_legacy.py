def prune(G):
    removed = []
    while True:
        referenced = {label for n in G for label in G.nodes[n].get("data", [])}
        unused = [n for n in G if n.startswith("//legacy/") and G.out_degree(n) == 0 and n not in referenced]
        if not unused:
            return sorted(removed)
        G.remove_nodes_from(unused)
        removed += unused
