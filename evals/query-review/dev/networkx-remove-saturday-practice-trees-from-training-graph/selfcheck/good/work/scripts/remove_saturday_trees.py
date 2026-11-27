"""Remove the trees Saturday's practice session added (PRAC-SAT-*) and their edges."""


def change(G):
    G.remove_nodes_from([n for n in list(G) if n.startswith("PRAC-SAT-")])
