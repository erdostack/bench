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
