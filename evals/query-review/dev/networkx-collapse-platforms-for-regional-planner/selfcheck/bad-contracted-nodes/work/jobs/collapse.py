import json
from pathlib import Path

import networkx as nx


def load(path="data/network.json"):
    return nx.node_link_graph(json.loads(Path(path).read_text()), directed=True, multigraph=False, edges="links")


def collapse_platforms(G: nx.DiGraph) -> nx.DiGraph:
    S = G.copy()
    S.remove_edges_from([(u, v) for u, v, d in G.edges(data=True) if d["kind"] != "run"])
    for n, d in list(G.nodes(data=True)):
        if d["kind"] == "platform":
            S = nx.contracted_nodes(S, d["station"], n, copy=False)
    for n in S.nodes:
        S.nodes[n].pop("contraction", None)
    return S
