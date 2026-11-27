"""Merge duplicate trader records (see docs/flows.md)."""


def merge_duplicates(G, pairs):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    groups = {}
    for x in list(parent):
        groups.setdefault(find(x), []).append(x)
    for members in groups.values():
        members = [m for m in members if m in G]
        if len(members) < 2:
            continue
        keep = min(members, key=lambda m: (G.nodes[m]["registered"], m))
        group = set(members)
        for drop in members:
            if drop == keep:
                continue
            for _, v, d in list(G.out_edges(drop, data=True)):
                if v in group:
                    continue
                _add(G, keep, v, d)
            for u, _, d in list(G.in_edges(drop, data=True)):
                if u in group:
                    continue
                _add(G, u, keep, d)
            G.remove_node(drop)
        if G.has_edge(keep, keep):
            G.remove_edge(keep, keep)
    return G


def _add(G, u, v, d):
    if G.has_edge(u, v):
        G[u][v]["tonnes"] += d["tonnes"]
        G[u][v]["deals"] += d["deals"]
    else:
        G.add_edge(u, v, tonnes=d["tonnes"], deals=d["deals"])
