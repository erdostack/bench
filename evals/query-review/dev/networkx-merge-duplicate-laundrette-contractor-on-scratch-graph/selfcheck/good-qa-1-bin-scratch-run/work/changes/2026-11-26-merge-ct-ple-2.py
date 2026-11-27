"""Merge CT-PLE-2 (typed in twice from the contract PDFs) into CT-PLE."""


def run(G):
    moved = [(m, d) for m, _c, d in G.in_edges("CT-PLE-2", data=True) if d.get("kind") == "serviced_by"]
    for m, d in moved:
        G.add_edge(m, "CT-PLE", **d)
    G.remove_node("CT-PLE-2")
    return len(moved)
