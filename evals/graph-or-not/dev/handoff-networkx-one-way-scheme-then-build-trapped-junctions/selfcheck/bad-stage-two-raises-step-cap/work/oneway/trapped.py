"""Which junctions does a draft one-way scheme trap?"""
from collections import deque

MAX_STEPS = 500


def _moves(conn):
    out = {}
    for a, b, oneway in conn.execute("SELECT a, b, oneway FROM segment"):
        if oneway in (0, 1):
            out.setdefault(a, []).append(b)
        if oneway in (0, -1):
            out.setdefault(b, []).append(a)
    return out


def trapped_junctions(conn):
    """Junctions from which the ring road cannot be reached."""
    ring = {j for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 1")}
    moves = _moves(conn)
    trapped = []
    for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 0 ORDER BY junction_id"):
        seen, queue, found = {j}, deque([(j, 0)]), False
        while queue and not found:
            here, steps = queue.popleft()
            if steps >= MAX_STEPS:
                continue
            for nxt in moves.get(here, ()):
                if nxt in ring:
                    found = True
                    break
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
        if not found:
            trapped.append(j)
    return trapped
