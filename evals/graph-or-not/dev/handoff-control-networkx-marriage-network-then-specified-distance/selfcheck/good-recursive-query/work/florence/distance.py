SQL = """
WITH RECURSIVE edge(x, y) AS (
    SELECT family_a, family_b FROM marriage UNION SELECT family_b, family_a FROM marriage
),
walk(family, steps) AS (
    SELECT ?, 0
    UNION
    SELECT edge.y, walk.steps + 1 FROM walk JOIN edge ON edge.x = walk.family WHERE walk.steps < 16
)
SELECT MIN(steps) FROM walk WHERE family = ?
"""


def marriage_distance(conn, a, b):
    (steps,) = conn.execute(SQL, (a, b)).fetchone()
    return steps
