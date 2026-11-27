import networkx as nx

from travel.graph import load_graph, load_merges
from travel.merge import merge_grounds


def build():
    return merge_grounds(load_graph(), load_merges())


def route_km(G: nx.Graph, home: str, away: str) -> float:
    return nx.shortest_path_length(G, home, away, weight="km")
