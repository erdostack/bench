"""Move the B1 learners of DEMO-D2 to DEMO-D3 (open-day demo)."""


def change(G):
    movers = [u for u, v, a in G.edges(data=True)
              if v == "DEMO-D2" and a.get("kind") == "member_of" and G.nodes[u].get("level") == "B1"]
    for u in movers:
        G.remove_edge(u, "DEMO-D2")
        G.add_edge(u, "DEMO-D3", kind="member_of")
    print(f"moved {len(movers)}")
