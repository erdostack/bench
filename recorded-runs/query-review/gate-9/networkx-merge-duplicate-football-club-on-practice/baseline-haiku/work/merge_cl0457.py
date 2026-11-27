def change(G):
    keep, drop = "CL-0112", "CL-0457"
    moved = []
    for u, v, d in list(G.in_edges(drop, data=True)):
        if d.get("kind") == "of_club":
            G.add_edge(u, keep, **d)
            moved.append(f"{u} of_club -> {keep}")
        elif d.get("kind") == "affiliated_to":
            if u != keep:
                G.add_edge(u, keep, **d)
            moved.append(f"{u} affiliated_to -> {keep}")
    for u, v, d in list(G.out_edges(drop, data=True)):
        if d.get("kind") == "home_ground":
            G.add_edge(keep, v, **d)
            moved.append(f"{keep} home_ground {v} since {d.get('since')}")
        elif d.get("kind") == "affiliated_to":
            if v != keep:
                G.add_edge(keep, v, **d)
            moved.append(f"{keep} affiliated_to {v}")
    G.remove_node(drop)
    return "merged CL-0457 into CL-0112:\n  " + "\n  ".join(moved)
