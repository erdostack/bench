"""Reach queries over the marriage network (tables as in db/schema.sql)."""

_FAMILIES_WITHIN = """
WITH RECURSIVE
    ties(a, b) AS (
        SELECT family_a, family_b FROM marriage_tie
        UNION
        SELECT family_b, family_a FROM marriage_tie
    ),
    walk(name, depth) AS (
        SELECT ?, 0
        UNION
        SELECT ties.b, walk.depth + 1
        FROM walk JOIN ties ON ties.a = walk.name
        WHERE walk.depth < ?
    )
SELECT DISTINCT name FROM walk WHERE name <> ? ORDER BY name
"""


def families_within(conn, family, k):
    """Sorted list of the other families reachable from `family` through at most `k` marriage ties.

    A tie joins two families in either direction. The family itself is never in the list;
    the list is empty when nothing is reachable, including for k = 0 or an unknown family.
    """
    if k <= 0:
        return []
    return [name for (name,) in conn.execute(_FAMILIES_WITHIN, (family, k, family))]
