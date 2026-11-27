"""The permission check."""


def is_inside(conn, group_id, container_id):
    """True if group_id is container_id or is nested in it at any depth."""
    if group_id == container_id:
        return True
    if conn.execute("SELECT 1 FROM reach WHERE ancestor_id = ? AND descendant_id = ?", (container_id, group_id)).fetchone():
        return True
    since = conn.execute("SELECT value FROM job_state WHERE key = 'reach_refreshed_at'").fetchone()[0]
    fresh = conn.execute("SELECT parent_id, child_id FROM group_edges WHERE added_at > ?", (since,)).fetchall()
    for parent, child in fresh:                       # nestings added since the last refresh
        if (parent == container_id or conn.execute(
                "SELECT 1 FROM reach WHERE ancestor_id = ? AND descendant_id = ?", (container_id, parent)).fetchone()) and (
                child == group_id or conn.execute(
                    "SELECT 1 FROM reach WHERE ancestor_id = ? AND descendant_id = ?", (child, group_id)).fetchone()):
            return True
    return False
