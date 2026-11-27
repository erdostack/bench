"""Nightly prune of the interaction network (docs/pruning.md)."""
import json
from datetime import date
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data" / "network.json"
YEARS = 10


def prune(G, cutoff):
    """Remove interactions and species not seen since `cutoff` (ISO date), then species left without partners."""
    stale_edges = [(u, v) for u, v, seen in G.edges(data="seen") if seen < cutoff]
    G.remove_edges_from(stale_edges)
    stale_nodes = [n for n, seen in G.nodes(data="last_seen") if seen < cutoff]
    G.remove_nodes_from(stale_nodes)
    return len(stale_edges), len(stale_nodes)


def main():
    G = nx.node_link_graph(json.loads(DATA.read_text()), edges="links")
    today = date.today()
    cutoff = today.replace(year=today.year - YEARS).isoformat()
    removed = prune(G, cutoff)
    DATA.write_text(json.dumps(nx.node_link_data(G, edges="links")))
    print("pruned", removed)


if __name__ == "__main__":
    main()
