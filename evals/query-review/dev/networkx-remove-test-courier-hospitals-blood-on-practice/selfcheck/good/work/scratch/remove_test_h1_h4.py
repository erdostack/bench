"""Remove the exercise hospitals TEST-H1 to TEST-H4 (and so their routes)."""


def run(G):
    gone = [f"TEST-H{i}" for i in range(1, 5)]
    G.remove_nodes_from(gone)
    return f"removed {len(gone)} places"
