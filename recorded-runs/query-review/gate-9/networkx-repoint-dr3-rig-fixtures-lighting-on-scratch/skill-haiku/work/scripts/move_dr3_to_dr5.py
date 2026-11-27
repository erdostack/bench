"""Scratch re-patch: move every fixture fed by DR-3 over to DR-5, keeping each circuit number.

Only the fed_by edge changes. Nothing else in the graph is touched.
"""

SRC, DST = "DR-3", "DR-5"


def run(G):
    moves = [(u, dict(d)) for u, v, d in G.in_edges(SRC, data=True) if d.get("kind") == "fed_by"]
    used = {d.get("circuit") for u, v, d in G.in_edges(DST, data=True) if d.get("kind") == "fed_by"}
    clashes = {d["circuit"] for _, d in moves} & used
    if clashes:
        raise RuntimeError(f"circuit clash on {DST}: {sorted(clashes)}")
    for u, d in moves:
        G.remove_edge(u, SRC)
        G.add_edge(u, DST, **d)
    return f"moved {len(moves)} fixtures from {SRC} to {DST}, circuits kept"
