def change(G):
    demo = [n for n in G.nodes if str(n).startswith("DEMO-")]
    G.remove_nodes_from(demo)
    return f"removed {len(demo)} DEMO- shops and their links"
