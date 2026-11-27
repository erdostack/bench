"""Drop weak similarity links without changing any shelf.

The shelf shows each playlist's three strongest links (docs/shelf.md), so a link under min_weight is
kept when it is one of the three strongest of either of its playlists.
"""


def prune_weak(G, min_weight=0.2):
    protected = set()
    for n in G:
        top = sorted(G[n].items(), key=lambda kv: kv[1]["weight"], reverse=True)[:3]
        protected.update(frozenset((n, m)) for m, _ in top)
    weak = [(a, b) for a, b, w in G.edges(data="weight")
            if w < min_weight and frozenset((a, b)) not in protected]
    G.remove_edges_from(weak)
    return len(weak)
