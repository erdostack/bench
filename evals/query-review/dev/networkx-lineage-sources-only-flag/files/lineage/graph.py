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


def upstream(G, name):
    """Every dataset that `name` is built from, directly or indirectly, sorted. `name` is not listed."""
    seen = set()

    def visit(node):
        for parent in G.predecessors(node):
            if parent not in seen:
                seen.add(parent)
                visit(parent)

    visit(name)
    seen.discard(name)
    return sorted(seen)


def downstream_count(G, name):
    """How many datasets are built from `name`, directly or indirectly."""
    return len(nx.descendants(G, name))


def owners(G, names):
    return sorted({G.nodes[n]["owner"] for n in names})
