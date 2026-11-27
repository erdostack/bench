def prune(G):
    removed = []
    while True:
        unused = [n for n in G if n.startswith("//legacy/") and G.in_degree(n) == 0]
        if not unused:
            return sorted(removed)
        G.remove_nodes_from(unused)
        removed += unused
