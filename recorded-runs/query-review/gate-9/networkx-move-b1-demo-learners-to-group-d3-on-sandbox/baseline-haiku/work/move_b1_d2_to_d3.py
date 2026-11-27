"""Move the B1 learners in DEMO-D2 to DEMO-D3 (sandbox only). A2 and B2 learners stay in DEMO-D2."""


def change(G):
    moved = []
    for learner in [n for n, d in G.nodes(data=True) if d.get("kind") == "learner"]:
        if G.nodes[learner].get("level") != "B1":
            continue
        for _, group, d in list(G.out_edges(learner, data=True)):
            if d.get("kind") == "member_of" and group == "DEMO-D2":
                attrs = dict(d)
                G.remove_edge(learner, group)
                G.add_edge(learner, "DEMO-D3", **attrs)
                moved.append(learner)
    print(f"moved {len(moved)} B1 learners from DEMO-D2 to DEMO-D3: {', '.join(sorted(moved))}")
