"""Next term's trial allocation: the Otters' Eastgate lane-3 hires go to lane 5."""


def run(G):
    moved = 0
    for hire, lane, d in list(G.edges(data=True)):
        if lane == "POOL-EAST-L3" and d.get("kind") == "on_lane":
            attrs = dict(G.edges[hire, "POOL-EAST-L3"])
            G.remove_edge(hire, "POOL-EAST-L3")
            G.add_edge(hire, "POOL-EAST-L5", **attrs)
            moved += 1
    return moved
