"""Prepare the sewer graph for a solver run."""
import csv

import networkx as nx


def read_pairs(path):
    """[(keep, drop), ...] from data/duplicates.csv."""
    with open(path, newline="") as f:
        return [(row["keep"], row["drop"]) for row in csv.DictReader(f)]


def merge_duplicates(G, pairs):
    """Return a new DiGraph in which every duplicate manhole in `pairs` is folded into the manhole it repeats.

    Chains (A,B) and (B,C) resolve to A (docs/model.md). A pipe whose two ends fold into the same manhole
    (the digitiser's link between two records, in either direction) is dropped: the solver rejects
    self-loops. A pipe the kept manhole already has keeps the kept manhole's attributes."""
    up = {drop: keep for keep, drop in pairs}

    def survivor(n):
        seen = set()
        while n in up and n not in seen:
            seen.add(n)
            n = up[n]
        return n

    H = nx.DiGraph()
    H.add_nodes_from((n, dict(d)) for n, d in G.nodes(data=True) if n not in up)
    kept_first = sorted(G.edges(data=True), key=lambda e: (e[0] in up or e[1] in up))
    for a, b, d in kept_first:
        u, v = survivor(a), survivor(b)
        if u == v or H.has_edge(u, v):
            continue
        H.add_edge(u, v, **d)
    return H


def drop_isolated(G):
    """Manholes with no pipe at all are left out of the solver graph."""
    H = G.copy()
    H.remove_nodes_from([n for n in G if G.degree(n) == 0])
    return H
