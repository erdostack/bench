"""Category tree helpers for the menu and the admin screens."""

SUBTREE = """
WITH RECURSIVE sub(id, depth) AS (
    SELECT id, 0 FROM categories WHERE id = :root
    UNION ALL
    SELECT c.id, s.depth + 1 FROM sub s JOIN categories c ON c.parent_id = s.id
    LIMIT 2000
)
SELECT id FROM sub ORDER BY depth, id
"""


def subtree_ids(conn, root):
    """Ids of `root` and every category below it, nearest levels first."""
    return [r[0] for r in conn.execute(SUBTREE, {"root": root})]


def breadcrumbs(conn, category_id):
    """Names from the top of the tree down to `category_id`."""
    rows = conn.execute(
        """WITH RECURSIVE up(id, parent_id, name, n) AS (
               SELECT id, parent_id, name, 0 FROM categories WHERE id = ?
               UNION ALL
               SELECT c.id, c.parent_id, c.name, u.n + 1 FROM up u JOIN categories c ON c.id = u.parent_id)
           SELECT name FROM up ORDER BY n DESC""", (category_id,)).fetchall()
    return [r[0] for r in rows]


def visible_children(conn, parent_id):
    return conn.execute("SELECT id, name FROM categories WHERE parent_id = ? AND archived = 0 ORDER BY name",
                        (parent_id,)).fetchall()
