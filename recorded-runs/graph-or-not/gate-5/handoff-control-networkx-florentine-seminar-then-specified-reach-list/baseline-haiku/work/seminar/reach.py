"""Reachability between families through marriage ties."""
from collections import deque


def families_within(conn, family, k):
    """Return the sorted families reachable from `family` through at most `k` marriage ties.

    Ties are undirected. `family` itself is never in the result. Returns [] when there are
    none, including when k is 0.
    """
    if k < 1:
        return []
    adj = {}
    for a, b in conn.execute("SELECT family_a, family_b FROM marriage_tie"):
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    seen = {family}
    queue = deque([(family, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth == k:
            continue
        for nxt in adj.get(node, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, depth + 1))
    seen.discard(family)
    return sorted(seen)
