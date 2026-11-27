"""Reach panel for the family pages: which families a family can reach through marriage ties."""

_REACH_SQL = """
WITH RECURSIVE
edge(a, b) AS (
    SELECT family_a, family_b FROM marriage_tie
    UNION ALL
    SELECT family_b, family_a FROM marriage_tie
),
walk(name, depth) AS (
    SELECT ?, 0
    UNION
    SELECT edge.b, walk.depth + 1
    FROM walk JOIN edge ON edge.a = walk.name
    WHERE walk.depth < ?
)
SELECT DISTINCT name FROM walk WHERE name <> ?
"""


def families_within(conn, family, k):
    """Sorted names of the other families reachable from `family` through at most `k` marriage ties.

    A tie joins two families either way. The family itself is never in the result; the result is
    empty when there is nothing reachable, including for k = 0.
    """
    if k < 1:
        return []
    rows = conn.execute(_REACH_SQL, (family, k, family)).fetchall()
    return sorted(name for (name,) in rows)
