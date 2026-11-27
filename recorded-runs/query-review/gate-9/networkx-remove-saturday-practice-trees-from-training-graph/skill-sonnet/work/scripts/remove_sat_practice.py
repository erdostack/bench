"""Remove saturday's survey-practice trees (PRAC-SAT-*) and their edges from the training graph.
Run: bin/tg run training scripts/remove_sat_practice.py
PRAC-BASE trees, PRAC-ST streets and volunteers are kept."""


def change(G):
    for n in [n for n, a in G.nodes(data=True) if a.get("kind") == "tree" and str(n).startswith("PRAC-SAT-")]:
        G.remove_node(n)  # also removes its on_street and surveyed edges
