"""Introductions between two members, for the newcomer buddy panel."""

# The welfare lead's rule: two members are linked only if they met in at least this many contexts.
MIN_CONTEXTS = 3

_SQL = """
WITH RECURSIVE
tie(x, y) AS (
    SELECT member_a, member_b FROM encounter
    GROUP BY member_a, member_b HAVING COUNT(*) >= :min_contexts
),
link(x, y) AS (
    SELECT x, y FROM tie
    UNION
    SELECT y, x FROM tie
),
walk(member, hops) AS (
    SELECT :a, 0
    UNION
    SELECT link.y, walk.hops + 1
    FROM walk JOIN link ON link.x = walk.member
    WHERE walk.hops < (SELECT COUNT(*) FROM member)
)
SELECT MIN(hops) FROM walk WHERE member = :b
"""


def introductions(conn, a, b):
    """Number of introductions on the shortest chain from member a to member b.

    0 if a and b are the same member, None if no chain of ties (each a pair that met in at
    least MIN_CONTEXTS contexts) joins them.
    """
    if a == b:
        return 0
    (hops,) = conn.execute(_SQL, {"a": a, "b": b, "min_contexts": MIN_CONTEXTS}).fetchone()
    return hops
