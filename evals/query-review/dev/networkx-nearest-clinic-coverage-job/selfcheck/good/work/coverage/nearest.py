"""Referral clinic for every village."""
import networkx as nx


def nearest_clinics(G, clinics):
    """For every village, the clinic with the shortest drive and the drive in minutes.

    Returns {village: (clinic, minutes)}. When two clinics are equally near, the one with the smaller
    id wins. A village that cannot reach any clinic maps to None."""
    # One Dijkstra per clinic (roads are undirected, so clinic -> village is the same drive as village -> clinic)
    # instead of one per village and clinic. Clinics are visited in id order and only a strictly shorter drive
    # replaces the current best, which keeps the smaller-id rule on ties.
    out = {v: None for v, kind in G.nodes(data="kind") if kind == "village"}
    for c in sorted(clinics):
        for v, t in nx.single_source_dijkstra_path_length(G, c, weight="minutes").items():
            if v in out and (out[v] is None or t < out[v][1]):
                out[v] = (c, t)
    return out
