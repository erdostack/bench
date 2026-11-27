"""Everything that depends, directly or through other versions, on one artifact version."""

LEVEL = "SELECT version_id FROM dependency WHERE depends_on_id IN ({})"


def dependents(cur, version_id):
    seen, frontier = set(), [version_id]
    while frontier:
        cur.execute(LEVEL.format(",".join(["%s"] * len(frontier))), frontier)
        frontier = [v for (v,) in cur.fetchall() if v not in seen]
        seen.update(frontier)
    seen.discard(version_id)
    return seen
