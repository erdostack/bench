"""Merge duplicate lab LAB-31 into LAB-07 (scratch only). Re-points every sent_to edge, keeping attributes,
then removes LAB-31 with its in_city edge. Refuses to run if any case would end up with two sent_to edges."""


def change(G):
    keep, dup = "LAB-07", "LAB-31"
    assert G.nodes[dup]["kind"] == "lab" and G.nodes[keep]["kind"] == "lab"
    moved = [(case, dict(d)) for case, _, d in G.in_edges(dup, data=True)]
    assert all(d["kind"] == "sent_to" for _, d in moved), "unexpected edge kind into the duplicate"
    assert not any(G.has_edge(case, keep) for case, _ in moved), "a case is sent to both labs"
    for case, attrs in moved:
        G.add_edge(case, keep, **attrs)
    G.remove_node(dup)
    return {"re_pointed": len(moved)}
