"""Lineage helpers for the catalogue page."""
import json

import networkx as nx


def load_catalog(path):
    """DiGraph with an edge input -> output for every dataset input; node attribute `owner`."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    G = nx.DiGraph()
    for ds in raw["datasets"]:
        G.add_node(ds["name"], owner=ds["owner"])
        for src in ds["inputs"]:
            G.add_edge(src, ds["name"])
    return G


def upstream(G, name, sources_only=False):
    """Every dataset that `name` is built from, directly or indirectly, sorted. `name` is not listed."""
    if sources_only:
        return sorted(p for p in G.predecessors(name) if G.in_degree(p) == 0)
    return sorted(nx.ancestors(G, name))


def downstream_count(G, name):
    """How many datasets are built from `name`, directly or indirectly."""
    return len(nx.descendants(G, name))


def owners(G, names):
    return sorted({G.nodes[n]["owner"] for n in names})
