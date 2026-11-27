"""Access checks for the document service."""
from collections import deque

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


def explain_access(conn, user_id, resource_id):
    """The shortest chain of group ids that gives user_id a grant on resource_id: a group the user is directly in
    first, the group holding the grant last, each nested in the next. None without access.

    Breadth-first over the nesting, one level at a time, never expanding a group twice: nesting has loops and
    many routes to the same group, so listing paths would never finish on the real data."""
    holders = {g for (g,) in conn.execute("SELECT group_id FROM grants WHERE resource_id = ?", (resource_id,))}
    if not holders:
        return None
    start = sorted(g for (g,) in conn.execute("SELECT group_id FROM user_groups WHERE user_id = ?", (user_id,)))
    prev = {g: None for g in start}
    level = start
    while level:
        hit = next((g for g in level if g in holders), None)
        if hit is not None:
            chain = [hit]
            while prev[chain[-1]] is not None:
                chain.append(prev[chain[-1]])
            return chain[::-1]
        marks = ",".join("?" * len(level))
        nxt = []
        for child, parent in conn.execute(
                f"SELECT child_id, parent_id FROM group_nesting WHERE child_id IN ({marks}) ORDER BY child_id, parent_id", level):
            if parent not in prev:
                prev[parent] = child
                nxt.append(parent)
        level = nxt
    return None
