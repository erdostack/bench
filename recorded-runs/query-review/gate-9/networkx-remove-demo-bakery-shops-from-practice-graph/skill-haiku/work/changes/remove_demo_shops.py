"""Remove the DEMO- training shops from the practice graph, with their delivers edges.

Run as: bin/net practice changes/remove_demo_shops.py

A DEMO- shop is a node whose id starts with DEMO- (docs/network.md; bin/new-practice adds them).
Every edge touching one of them is removed with it. Depots and real shops are not changed.
"""


def change(G):
    demo = [n for n, d in G.nodes(data=True) if str(n).startswith("DEMO-") and d.get("kind") == "shop"]
    G.remove_nodes_from(demo)
    return f"removed {len(demo)} DEMO- shops and their edges"
