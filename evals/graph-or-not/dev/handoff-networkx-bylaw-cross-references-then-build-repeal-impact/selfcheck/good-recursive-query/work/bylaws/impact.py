QUERY = """
WITH RECURSIVE affected(id) AS (
    SELECT from_bylaw FROM reference WHERE to_bylaw = :x AND kind IN ('amends', 'depends_on')
    UNION
    SELECT r.from_bylaw FROM reference r JOIN affected a ON r.to_bylaw = a.id
    WHERE r.kind IN ('amends', 'depends_on')
)
SELECT id FROM affected WHERE id <> :x ORDER BY id
"""


def affected_by_repeal(conn, bylaw_id):
    return [r[0] for r in conn.execute(QUERY, {"x": bylaw_id})]
