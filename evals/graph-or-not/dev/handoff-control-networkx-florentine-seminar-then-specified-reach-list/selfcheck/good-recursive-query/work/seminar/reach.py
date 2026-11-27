SQL = """
WITH RECURSIVE tie(x, y) AS (
    SELECT family_a, family_b FROM marriage_tie UNION SELECT family_b, family_a FROM marriage_tie
),
reach(name, steps) AS (
    SELECT ?, 0
    UNION
    SELECT tie.y, reach.steps + 1 FROM reach JOIN tie ON tie.x = reach.name WHERE reach.steps < ?
)
SELECT DISTINCT name FROM reach WHERE name <> ? ORDER BY name
"""


def families_within(conn, family, k):
    return [n for (n,) in conn.execute(SQL, (family, k, family))]
