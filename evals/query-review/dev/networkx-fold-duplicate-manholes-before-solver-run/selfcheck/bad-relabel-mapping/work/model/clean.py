"""Prepare the sewer graph for a solver run."""
import csv


def read_pairs(path):
    """[(keep, drop), ...] from data/duplicates.csv."""
    with open(path, newline="") as f:
        return [(row["keep"], row["drop"]) for row in csv.DictReader(f)]


def merge_duplicates(G, pairs):
    """Return a new DiGraph in which every duplicate manhole in `pairs` is folded into the manhole it repeats."""
    import networkx as nx
    return nx.relabel_nodes(G, {drop: keep for keep, drop in pairs}, copy=True)


def drop_isolated(G):
    """Manholes with no pipe at all are left out of the solver graph."""
    H = G.copy()
    H.remove_nodes_from([n for n in G if G.degree(n) == 0])
    return H
