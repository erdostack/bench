def change(G):
    G.remove_nodes_from([n for n in list(G) if n.startswith("DEMO-")])
