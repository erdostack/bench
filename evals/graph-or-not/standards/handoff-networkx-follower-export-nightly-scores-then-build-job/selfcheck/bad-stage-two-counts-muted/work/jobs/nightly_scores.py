"""Nightly scores job: reach and ring for every account (docs/scores.md).

Run from cron after the export lands: python3 -m jobs.nightly_scores exports/
"""
import sys
from pathlib import Path

import networkx as nx

DAMPING = 0.85
STEPS = 20


def load(export_dir):
    """DiGraph follower -> followed, with every account; edge attribute muted."""
    d = Path(export_dir)
    g = nx.DiGraph()
    g.add_nodes_from(int(line) for line in open(d / "accounts.txt") if line.strip() and not line.startswith("#"))
    for line in open(d / "follows.edges"):
        if not line.strip() or line.startswith("#"):
            continue
        followed, follower, muted = line.split()       # header: followed_id follower_id muted
        g.add_edge(int(follower), int(followed), muted=muted == "1")
    return g


def reach(g):
    """PageRank as docs/scores.md: start 1/N, exactly STEPS steps."""
    live = nx.DiGraph()
    live.add_nodes_from(g)
    live.add_edges_from(g.edges())
    n = live.number_of_nodes()
    out = dict(live.out_degree())
    r = dict.fromkeys(live, 1.0 / n)
    for _ in range(STEPS):
        dangling = sum(r[v] for v in live if out[v] == 0)
        r = {v: (1 - DAMPING) / n + DAMPING * sum(r[u] / out[u] for u in live.predecessors(v)) + DAMPING * dangling / n
             for v in live}
    return r


def scores(export_dir):
    """{account_id: (ring_id, reach)}. Rings use every follow, muted ones included."""
    g = load(export_dir)
    ring = {}
    for i, comp in enumerate(nx.weakly_connected_components(g)):
        for v in comp:
            ring[v] = i
    r = reach(g)
    return {v: (ring[v], r[v]) for v in g}


if __name__ == "__main__":
    result = scores(sys.argv[1] if len(sys.argv) > 1 else "exports")
    print(len(result), "accounts scored")
