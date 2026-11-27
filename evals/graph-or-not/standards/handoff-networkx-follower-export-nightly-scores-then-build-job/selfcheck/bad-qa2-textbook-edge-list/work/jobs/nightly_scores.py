from pathlib import Path
import networkx as nx


def scores(export_dir):
    d = Path(export_dir)
    g = nx.read_edgelist(d / "follows.edges", comments="#", create_using=nx.DiGraph, nodetype=int, data=(("muted", int),))
    g.add_nodes_from(int(x) for x in open(d / "accounts.txt") if x.strip() and not x.startswith("#"))
    r = dict.fromkeys(g, 1 / g.number_of_nodes())
    n = g.number_of_nodes()
    for _ in range(20):
        dang = sum(r[v] for v in g if g.out_degree(v) == 0)
        r = {v: 0.15 / n + 0.85 * (sum(r[u] / g.out_degree(u) for u in g.predecessors(v)) + dang / n) for v in g}
    ring = {v: i for i, c in enumerate(nx.weakly_connected_components(g)) for v in c}
    return {v: (ring[v], r[v]) for v in g}
