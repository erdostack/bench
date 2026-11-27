"""Next term's trial allocation: the Otters' Eastgate lane-3 hires go to lane 5."""


def run(G):
    moved = 0
    for _club, hire, d in list(G.out_edges("CLUB-OTTERS", data=True)):
        if d.get("kind") == "booked" and G.has_edge(hire, "POOL-EAST-L3"):
            attrs = dict(G.edges[hire, "POOL-EAST-L3"])
            G.add_edge(hire, "POOL-EAST-L5", **attrs)
            moved += 1
    return moved
