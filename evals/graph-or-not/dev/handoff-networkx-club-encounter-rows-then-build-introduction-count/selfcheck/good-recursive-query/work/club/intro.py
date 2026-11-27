SQL = """
WITH RECURSIVE strong(x, y) AS (
    SELECT member_a, member_b FROM encounter GROUP BY member_a, member_b HAVING COUNT(*) >= 3
    UNION SELECT member_b, member_a FROM encounter GROUP BY member_a, member_b HAVING COUNT(*) >= 3
),
walk(m, steps) AS (
    SELECT ?, 0
    UNION
    SELECT strong.y, walk.steps + 1 FROM walk JOIN strong ON strong.x = walk.m WHERE walk.steps < 34
)
SELECT MIN(steps) FROM walk WHERE m = ?
"""


def introductions(conn, a, b):
    (steps,) = conn.execute(SQL, (a, b)).fetchone()
    return steps
