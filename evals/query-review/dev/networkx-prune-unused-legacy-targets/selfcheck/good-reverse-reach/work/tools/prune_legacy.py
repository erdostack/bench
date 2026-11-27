import networkx as nx


def prune(G):
    """Keep every legacy target reachable from a non-legacy target through deps or data references."""
    U = nx.DiGraph()
    U.add_nodes_from(G)
    U.add_edges_from(G.edges)
    for n in G:
        for lab in G.nodes[n].get("data", []):
            if lab in G:
                U.add_edge(n, lab)
    roots = [n for n in G if not n.startswith("//legacy/")]
    used = set(roots)
    for r in roots:
        used |= nx.descendants(U, r)
    gone = sorted(n for n in G if n not in used)
    G.remove_nodes_from(gone)
    return gone
