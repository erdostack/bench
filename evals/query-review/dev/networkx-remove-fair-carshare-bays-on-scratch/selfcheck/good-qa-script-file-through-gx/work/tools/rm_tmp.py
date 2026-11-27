fair = [n for n, d in G.nodes(data=True) if d.get("kind") == "temporary" and n.startswith("TMP-")]
print("removing", len(fair), "bays and", sum(G.degree(n) for n in fair), "links")
G.remove_nodes_from(fair)
