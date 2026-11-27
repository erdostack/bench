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
        H = nx.contracted_nodes(H, root(drop), drop, self_loops=False, copy=True)
    for _n, d in H.nodes(data=True):
        d.pop("contraction", None)
    for _a, _b, d in H.edges(data=True):
        d.pop("contraction", None)
    return H


def drop_isolated(G):
    H = G.copy()
    H.remove_nodes_from([n for n in G if G.degree(n) == 0])
    return H
