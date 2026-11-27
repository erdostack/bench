def change(G):
    for u, _v, d in list(G.in_edges("CL-0457", data=True)):
        if d["kind"] == "of_club":
            G.add_edge(u, "CL-0112", **d)
    for _u, v, d in list(G.out_edges("CL-0457", data=True)):
        if d["kind"] == "home_ground":
            G.add_edge("CL-0112", v, **d)
    G.remove_node("CL-0457")
