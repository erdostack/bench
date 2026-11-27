def change(G):
    todo = [(u, d) for u, v, d in G.edges(data=True)
            if v == "C-14" and d.get("kind") == "run_by" and "2026-12-01" <= G.nodes[u]["departs_on"] <= "2026-12-12"]
    for u, d in todo:
        G.remove_edge(u, "C-14")
        G.add_edge(u, "C-22", **d)
    print(len(todo), "departures moved")
    return len(todo)
