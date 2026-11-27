"""Exhibit pages (rendering only)."""
import networkx as nx

from society.data import load_attendance, women


def index_page():
    return {"women": women()}


def woman_page(name):
    return {"name": name, "events": sorted(e for w, e in load_attendance() if w == name)}


def circles_page(name):
    """Women ringed by how many shared events away from `name` they are: ring 1 shared an event with her,
    ring 2 shared an event with someone in ring 1, and so on out to the whole network."""
    g = nx.Graph()
    for w, e in load_attendance():
        g.add_edge(("woman", w), ("event", e))
    start = ("woman", name)
    if start not in g:
        raise KeyError(name)
    steps = {}
    for node, hops in nx.single_source_shortest_path_length(g, start).items():
        if node[0] == "woman" and hops > 0:
            steps.setdefault(hops // 2, []).append(node[1])  # woman -> event -> woman is 2 hops
    return {"name": name, "circles": [{"step": k, "women": sorted(v)} for k, v in sorted(steps.items())]}
