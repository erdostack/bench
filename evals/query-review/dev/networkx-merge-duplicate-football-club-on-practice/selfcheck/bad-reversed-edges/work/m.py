def change(G):
    for n in list(G.predecessors("CL-0457")) + list(G.successors("CL-0457")):
        d = G.edges[n, "CL-0457"] if G.has_edge(n, "CL-0457") else G.edges["CL-0457", n]
        G.add_edge(n, "CL-0112", **d)
    G.remove_node("CL-0457")
