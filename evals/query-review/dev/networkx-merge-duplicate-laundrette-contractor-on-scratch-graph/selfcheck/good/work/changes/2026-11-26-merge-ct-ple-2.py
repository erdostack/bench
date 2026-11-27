"""Merge CT-PLE-2 (typed in twice) into CT-PLE; serviced_by links keep contract and since."""


def run(G):
    moved = 0
    for m, _c, d in list(G.in_edges("CT-PLE-2", data=True)):
        G.add_edge(m, "CT-PLE", **d)
        moved += 1
    G.remove_node("CT-PLE-2")
    return moved
