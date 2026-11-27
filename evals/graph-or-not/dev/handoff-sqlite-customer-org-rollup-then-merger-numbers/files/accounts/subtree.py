"""The account page's group-structure panel. conn is a sqlite3 connection to orgbook.db."""

SUBTREE_SQL = """
WITH RECURSIVE sub(id, name, parent_id, depth) AS (
    SELECT id, name, parent_id, 0 FROM org WHERE id = :root
    UNION ALL
    SELECT o.id, o.name, o.parent_id, sub.depth + 1
    FROM org AS o JOIN sub ON o.parent_id = sub.id
    WHERE sub.depth < 30                      -- the CRM cannot make a loop, but never run away if it does
)
SELECT id, name, parent_id, depth FROM sub ORDER BY depth, name
"""


def subtree(conn, root_id):
    return conn.execute(SUBTREE_SQL, {"root": root_id}).fetchall()
