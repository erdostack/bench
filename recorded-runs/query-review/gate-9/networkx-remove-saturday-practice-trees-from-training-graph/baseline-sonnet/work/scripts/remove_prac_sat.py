"""Remove the PRAC-SAT- practice trees (and, with them, their edges) from the training graph."""


def change(G):
    G.remove_nodes_from([n for n in list(G.nodes) if str(n).startswith("PRAC-SAT-")])
