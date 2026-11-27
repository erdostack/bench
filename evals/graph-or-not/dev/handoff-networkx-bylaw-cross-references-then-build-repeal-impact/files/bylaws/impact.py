"""Which bylaws a repeal would touch."""

MAX_LEVELS = 3   # deeper searches timed out the page (one query per level, see #212)


def affected_by_repeal(conn, bylaw_id):
    """Sorted ids of the bylaws that refer to bylaw_id, directly or through other bylaws."""
    found = set()
    frontier = {bylaw_id}
    for _ in range(MAX_LEVELS):
        if not frontier:
            break
        marks = ",".join("?" * len(frontier))
        rows = conn.execute(f"SELECT from_bylaw FROM reference WHERE to_bylaw IN ({marks})", sorted(frontier))
        frontier = {r[0] for r in rows} - found - {bylaw_id}
        found |= frontier
    return sorted(found)
