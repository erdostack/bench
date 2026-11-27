import csv

import networkx as nx


def read_pairs(path):
    with open(path, newline="") as f:
        return [(row["keep"], row["drop"]) for row in csv.DictReader(f)]


def merge_duplicates(G, pairs):
    up = {d: k for k, d in pairs}

    def root(n):
        while n in up:
            n = up[n]
        return n

    H = G.copy()
    for _keep, drop in pairs:
        keep = root(drop)
        for _, nbr, d in list(H.out_edges(drop, data=True)):
            if nbr != keep and not H.has_edge(keep, nbr):
                H.add_edge(keep, nbr, **d)
        for nbr, _, d in list(H.in_edges(drop, data=True)):
            if not H.has_edge(nbr, keep):
                H.add_edge(nbr, keep, **d)
        H.remove_node(drop)
    return H


def drop_isolated(G):
    H = G.copy()
    H.remove_nodes_from([n for n in G if G.degree(n) == 0])
    return H
