"""Access checks for the document service."""

MEMBER_OF = """
WITH RECURSIVE mine(group_id) AS (
    SELECT group_id FROM user_groups WHERE user_id = :user
    UNION
    SELECT n.parent_id FROM mine m JOIN group_nesting n ON n.child_id = m.group_id
)
SELECT 1 FROM grants g JOIN mine m ON m.group_id = g.group_id
WHERE g.resource_id = :resource
LIMIT 1
"""


def can_access(conn, user_id, resource_id):
    """True when one of the user's groups, directly or through nesting, holds a grant on the resource."""
    return conn.execute(MEMBER_OF, {"user": user_id, "resource": resource_id}).fetchone() is not None


CHAIN = """
WITH RECURSIVE walk(group_id, path, n) AS (
    SELECT group_id, ',' || group_id || ',', 1 FROM user_groups WHERE user_id = :user
    UNION ALL
    SELECT gn.parent_id, w.path || gn.parent_id || ',', w.n + 1
    FROM walk w JOIN group_nesting gn ON gn.child_id = w.group_id
    WHERE instr(w.path, ',' || gn.parent_id || ',') = 0
)
SELECT path FROM walk WHERE group_id IN (SELECT group_id FROM grants WHERE resource_id = :resource)
ORDER BY n LIMIT 1
"""


def explain_access(conn, user_id, resource_id):
    row = conn.execute(CHAIN, {"user": user_id, "resource": resource_id}).fetchone()
    return [int(x) for x in row[0].strip(",").split(",")] if row else None
