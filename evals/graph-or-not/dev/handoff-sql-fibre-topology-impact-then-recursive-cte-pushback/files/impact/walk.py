"""Which customer-facing devices lose service when a span fails.

Walks outward from the failed span, one query per hop, and keeps every device that can no longer reach a core
device. Slow on big rings; see the NOC tickets.
"""

CORE = "SELECT id FROM device WHERE kind = 'core'"
NEIGHBOURS = """
    SELECT CASE WHEN a_end = ANY(%(frontier)s) THEN b_end ELSE a_end END
    FROM link
    WHERE status = 'up' AND id <> %(failed)s AND (a_end = ANY(%(frontier)s) OR b_end = ANY(%(frontier)s))
"""


def reachable_from_core(cur, failed_link_id):
    cur.execute(CORE)
    seen = {r[0] for r in cur.fetchall()}
    frontier = list(seen)
    while frontier:
        cur.execute(NEIGHBOURS, {"frontier": frontier, "failed": failed_link_id})
        frontier = [d for (d,) in cur.fetchall() if d not in seen]
        seen.update(frontier)
    return seen


def impact(cur, failed_link_id):
    alive = reachable_from_core(cur, failed_link_id)
    cur.execute("SELECT id FROM device WHERE customer_facing")
    return sorted(d for (d,) in cur.fetchall() if d not in alive)
