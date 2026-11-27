"""Who to tell about a new street works permit."""

# "Near" is not defined anywhere yet; assumed to be this many junction hops from the works.
# Confirm the real rule (hops or metres) with whoever owns the notification policy.
DEFAULT_HOPS = 3

_NEARBY_OPERATORS = """
WITH RECURSIVE reach(junction_id, hops) AS (
    SELECT j1, 0 FROM segment WHERE segment_id = :segment_id
    UNION
    SELECT j2, 0 FROM segment WHERE segment_id = :segment_id
    UNION
    -- UNION (not UNION ALL) drops repeated (junction, hops) rows, so loops cannot run away;
    -- the hops bound stops the walk.
    SELECT CASE WHEN s.j1 = r.junction_id THEN s.j2 ELSE s.j1 END, r.hops + 1
    FROM reach r
    JOIN segment s ON s.j1 = r.junction_id OR s.j2 = r.junction_id
    WHERE r.hops < :hops
),
near AS (SELECT DISTINCT junction_id FROM reach)
SELECT DISTINCT sr.operator
FROM segment s
JOIN segment_route sr ON sr.segment_id = s.segment_id
WHERE s.j1 IN (SELECT junction_id FROM near)
   OR s.j2 IN (SELECT junction_id FROM near)
ORDER BY sr.operator
"""


def operators_to_notify(conn, segment_id, hops=DEFAULT_HOPS):
    """Bus operators with a route on any segment within `hops` junctions of the works segment."""
    rows = conn.execute(_NEARBY_OPERATORS, {"segment_id": segment_id, "hops": hops})
    return [r[0] for r in rows]
