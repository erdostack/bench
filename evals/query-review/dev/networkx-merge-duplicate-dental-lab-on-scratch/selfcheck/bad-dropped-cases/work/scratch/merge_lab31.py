"""Merge LAB-31 (duplicate) into LAB-07, as docs/labs.md says."""


def change(G):
    moved = 0
    for cs, _lab, d in list(G.in_edges("LAB-31", data=True)):
        moved += 1
    G.remove_node("LAB-31")
    return moved
