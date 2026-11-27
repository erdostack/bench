"""Similarity between two playlists: Jaccard overlap of their listeners over the last 90 days."""
import csv
from collections import defaultdict
from itertools import combinations

import networkx as nx


def build_graph(counts_path):
    listeners = defaultdict(set)
    with open(counts_path, newline="") as f:
        for row in csv.DictReader(f):
            listeners[row["playlist_id"]].add(row["user_id"])
    G = nx.Graph()
    G.add_nodes_from(listeners)
    by_user = defaultdict(list)
    for p, us in listeners.items():
        for u in us:
            by_user[u].append(p)
    pairs = set()
    for ps in by_user.values():
        pairs.update(combinations(sorted(ps), 2))
    for a, b in pairs:
        w = len(listeners[a] & listeners[b]) / len(listeners[a] | listeners[b])
        G.add_edge(a, b, weight=round(w, 6))
    return G
