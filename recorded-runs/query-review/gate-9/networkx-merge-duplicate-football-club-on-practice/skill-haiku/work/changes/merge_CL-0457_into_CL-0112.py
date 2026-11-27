"""Merge club CL-0457 (Hollybank Rovers JFC, a duplicate import) into CL-0112 (Hollybank Rovers).

Run as: bin/graph practice apply changes/merge_CL-0457_into_CL-0112.py

Every edge touching CL-0457 is re-pointed at CL-0112 with its kind and attributes kept:
teams (of_club), home grounds (home_ground) and affiliations in both directions (affiliated_to).
CL-0112 keeps its own name, founded year and edges. CL-0457 is then removed.
"""

SRC = "CL-0457"
DST = "CL-0112"


def change(G):
    assert G.nodes[SRC]["kind"] == "club" and G.nodes[DST]["kind"] == "club"
    moved, skipped = [], []

    for u, _v, d in list(G.in_edges(SRC, data=True)):
        if u == DST:
            skipped.append((u, SRC, d["kind"]))  # would become a self-loop
        elif G.has_edge(u, DST) and G.edges[u, DST].get("kind") == d["kind"]:
            skipped.append((u, SRC, d["kind"]))  # already on DST, keep DST's copy
        else:
            G.add_edge(u, DST, **d)
            moved.append((u, DST, d["kind"]))

    for _u, v, d in list(G.out_edges(SRC, data=True)):
        if v == DST:
            skipped.append((SRC, v, d["kind"]))
        elif G.has_edge(DST, v) and G.edges[DST, v].get("kind") == d["kind"]:
            skipped.append((SRC, v, d["kind"]))
        else:
            G.add_edge(DST, v, **d)
            moved.append((DST, v, d["kind"]))

    G.remove_node(SRC)
    return f"merged {SRC} into {DST}: {len(moved)} edges re-pointed {moved}, skipped {skipped}, removed {SRC}"
