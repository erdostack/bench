"""Merge CL-0457 (duplicate Hollybank Rovers) into CL-0112: move every edge, then drop CL-0457."""


def change(G):
    old, new = "CL-0457", "CL-0112"
    moved = 0
    for u, _v, d in list(G.in_edges(old, data=True)):
        G.add_edge(u, new, **d)
        moved += 1
    for _u, v, d in list(G.out_edges(old, data=True)):
        G.add_edge(new, v, **d)
        moved += 1
    G.remove_node(old)
    return f"moved {moved} edges, removed {old}"
