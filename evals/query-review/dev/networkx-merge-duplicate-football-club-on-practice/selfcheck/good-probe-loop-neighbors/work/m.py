def change(G):
    for p in list(G.predecessors("CL-0457")):
        G.add_edge(p, "CL-0112", **G["CL-0457"].get(p, {}) , **G.edges[p, "CL-0457"]) if False else G.add_edge(p, "CL-0112", **G.edges[p, "CL-0457"])
    for s in list(G.successors("CL-0457")):
        G.add_edge("CL-0112", s, **G.edges["CL-0457", s])
    G.remove_node("CL-0457")
    return "ok"
