"""Road segments that would cut people off if snow closed them."""
from collections import deque

MAX_DETOUR_HOPS = 40


def _neighbours(conn):
    adj = {}
    for sid, a, b in conn.execute("SELECT id, a, b FROM segment"):
        adj.setdefault(a, {})[b] = sid
        adj.setdefault(b, {})[a] = sid
    return adj


def _detour_exists(adj, start, goal, banned):
    seen, queue = {start}, deque([(start, 0)])
    while queue:
        node, hops = queue.popleft()
        if node == goal:
            return True
        if hops == MAX_DETOUR_HOPS:
            continue
        for nxt, sid in adj.get(node, {}).items():
            if sid != banned and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, hops + 1))
    return False


def cutoff_segments(conn):
    """Sorted ids of segments with no way round them."""
    adj = _neighbours(conn)
    out = []
    for sid, a, b in conn.execute("SELECT id, a, b FROM segment").fetchall():
        if not _detour_exists(adj, a, b, sid):
            out.append(sid)
    return sorted(out)
