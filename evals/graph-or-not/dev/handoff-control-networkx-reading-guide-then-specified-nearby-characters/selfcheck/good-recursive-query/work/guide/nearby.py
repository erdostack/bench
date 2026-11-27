QUERY = """
WITH RECURSIVE edge(x, y) AS (
    SELECT a, b FROM tie UNION ALL SELECT b, a FROM tie
), walk(id, depth) AS (
    SELECT id, 0 FROM character WHERE name = :name
    UNION
    SELECT edge.y, walk.depth + 1 FROM walk JOIN edge ON edge.x = walk.id WHERE walk.depth < :steps
)
SELECT DISTINCT c.name FROM walk JOIN character c ON c.id = walk.id WHERE c.name <> :name
"""


def characters_within(conn, name, steps):
    return [n for (n,) in conn.execute(QUERY, {"name": name, "steps": steps})]
