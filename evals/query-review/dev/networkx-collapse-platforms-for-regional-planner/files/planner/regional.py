"""Regional planner: travel times between stations on the station-level graph."""
import networkx as nx


def check(S: nx.DiGraph) -> None:
    for u, v, d in S.edges(data=True):
        if u == v:
            raise ValueError(f"{u}: an edge from a station to itself is not a journey")
        if "minutes" not in d:
            raise ValueError(f"{u}->{v}: no minutes")
    for n, d in S.nodes(data=True):
        if d.get("kind") != "station":
            raise ValueError(f"{n} is not a station")


def travel_minutes(S: nx.DiGraph, a: str, b: str) -> int:
    return nx.shortest_path_length(S, a, b, weight="minutes")


def direct_destinations(S: nx.DiGraph, a: str) -> int:
    """'Direct trains to N places' on the station page."""
    return S.out_degree(a)
