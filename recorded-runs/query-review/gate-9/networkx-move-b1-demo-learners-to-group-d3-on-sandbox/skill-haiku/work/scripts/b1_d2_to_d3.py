"""Demo timetable: move the B1 learners in DEMO-D2 to DEMO-D3. A2 and B2 learners stay in DEMO-D2."""

FROM, TO, LEVEL = "DEMO-D2", "DEMO-D3", "B1"


def change(G):
    movers = [l for l, _, d in G.in_edges(FROM, data=True)
              if d.get("kind") == "member_of" and G.nodes[l].get("level") == LEVEL]
    for l in movers:
        G.remove_edge(l, FROM)
        G.add_edge(l, TO, kind="member_of")
    print(f"moved {len(movers)} {LEVEL} learners from {FROM} to {TO}")
