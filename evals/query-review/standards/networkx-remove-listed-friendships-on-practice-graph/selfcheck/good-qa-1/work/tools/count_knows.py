"""Read-only: how many friendships a graph holds (run on both graphs to compare before the change)."""


def run(G):
    return sum(1 for _u, _v, d in G.edges(data=True) if d["kind"] == "knows")
