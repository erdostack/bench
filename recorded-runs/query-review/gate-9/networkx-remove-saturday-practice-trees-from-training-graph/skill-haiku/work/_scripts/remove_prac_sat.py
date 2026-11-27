def change(G):
    doomed = [n for n, a in G.nodes(data=True) if str(n).startswith("PRAC-SAT-") and a.get("kind") == "tree"]
    G.remove_nodes_from(doomed)
